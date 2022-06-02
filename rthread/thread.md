```cpp
//没有r13,因为sp的值就是r13
struct exception_stack_frame
{
    rt_uint32_t r0;
    rt_uint32_t r1;
    rt_uint32_t r2;
    rt_uint32_t r3;
    rt_uint32_t r12;
    rt_uint32_t lr; //r14
    rt_uint32_t pc; //r15
    rt_uint32_t psr;
};

struct stack_frame
{
    /* r4 ~ r11 register */
    rt_uint32_t r4;
    rt_uint32_t r5;
    rt_uint32_t r6;
    rt_uint32_t r7;
    rt_uint32_t r8;
    rt_uint32_t r9;
    rt_uint32_t r10;
    rt_uint32_t r11;

    struct exception_stack_frame exception_stack_frame;
};
```

## 线程调度
32位大小数组，数组每一项都是一个链表，存放的是同一优先级下所有已经就绪的线程
```cpp
rt_list_t rt_thread_priority_table[RT_THREAD_PRIORITY_MAX];
```

线程调度函数
```cpp
/**
 * This function will startup scheduler. It will select one thread
 * with the highest priority level, then switch to it.
 */
void rt_system_scheduler_start(void)
{
    register struct rt_thread *to_thread;
    register rt_ubase_t highest_ready_priority;

	// 从最高优先级开始遍历，直到找到第一个非空的数组项
    highest_ready_priority = __rt_ffs(rt_thread_ready_priority_group) - 1;

    /* 找到该数组项链表中的第一个元素 */
    to_thread = rt_list_entry(rt_thread_priority_table[highest_ready_priority].next,
                              struct rt_thread,
                              tlist);

    rt_current_thread = to_thread;

    /* switch to new thread */
    rt_hw_context_switch_to((rt_uint32_t)&to_thread->sp);

    /* never come back */
}

```

每隔固定时间会产生一个中断，检查当前线程时间片是否运行完，如果运行完，就切换
```cpp
/**
 * This function will notify kernel there is one tick passed. Normally,
 * this function is invoked by clock ISR.
 */
void rt_tick_increase(void)
{
    struct rt_thread *thread;

    /* increase the global tick */
    ++ rt_tick;

    /* check time slice */
    thread = rt_thread_self();

    -- thread->remaining_tick;
    if (thread->remaining_tick == 0)
    {
        /* change to initialized tick */
        thread->remaining_tick = thread->init_tick;

        /* yield */
        rt_thread_yield();
    }

    /* check timer */
    rt_timer_check();
}


/**
 * This function will let current thread yield processor, and scheduler will
 * choose a highest thread to run. After yield processor, the current thread is still in READY state.
 * 只是会从链表头挪到链表尾
 *
 * @return RT_EOK
 */
rt_err_t rt_thread_yield(void)
{
    register rt_base_t level;
    struct rt_thread *thread;

    /* disable interrupt */
    level = rt_hw_interrupt_disable();

    /* set to current thread */
    thread = rt_current_thread;

    /* if the thread stat is READY and on ready queue list */
    if ((thread->stat & RT_THREAD_STAT_MASK) == RT_THREAD_READY &&
        thread->tlist.next != thread->tlist.prev)
    {
        /* remove thread from thread list */
        rt_list_remove(&(thread->tlist));

        /* put thread to end of ready queue */
        rt_list_insert_before(&(rt_thread_priority_table[thread->current_priority]),
                              &(thread->tlist));

        /* enable interrupt */
        rt_hw_interrupt_enable(level);

        rt_schedule();

        return RT_EOK;
    }

    /* enable interrupt */
    rt_hw_interrupt_enable(level);

    return RT_EOK;
}
```


### 线程睡眠
```cpp
/**
 * This function will let current thread sleep for some ticks.
 */
rt_err_t rt_thread_sleep(rt_tick_t tick)
{
    register rt_base_t temp;
    struct rt_thread *thread;

    /* set to current thread */
    thread = rt_current_thread;

    /* suspend thread */
    rt_thread_suspend(thread); //从ready 链表中移 除

    /* reset the timeout of thread timer and start it */
    rt_timer_control(&(thread->thread_timer), RT_TIMER_CTRL_SET_TIME, &tick);
    rt_timer_start(&(thread->thread_timer));

    rt_schedule();

    return RT_EOK;
}
```

```cpp
/**
 * This function will check timer list, if a timeout event happens, the
 * corresponding timeout function will be invoked.
 */
void rt_timer_check(void)
{
    struct rt_timer *t;
    rt_tick_t current_tick;

    current_tick = rt_tick_get();


    while (!rt_list_isempty(&rt_timer_list[RT_TIMER_SKIP_LIST_LEVEL - 1]))
    {
        t = rt_list_entry(rt_timer_list[RT_TIMER_SKIP_LIST_LEVEL - 1].next,
                          struct rt_timer, row[RT_TIMER_SKIP_LIST_LEVEL - 1]);

        /*
         * It supposes that the new tick shall less than the half duration of
         * tick max.
         */
        if ((current_tick - t->timeout_tick) < RT_TICK_MAX / 2)
        {

            /* remove timer from timer list firstly */
            _rt_timer_remove(t);

            /* call timeout function */
            t->timeout_func(t->parameter);

        }
        else
            break;
    }
}
```


