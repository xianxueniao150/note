slf4j只是一个日志标准，并不是日志系统的具体实现
我们为什么要使用slf4j，举个例子：
我们自己的系统中使用了logback这个日志系统
我们的系统使用了A.jar，A.jar中使用的日志系统为log4j
我们的系统又使用了B.jar，B.jar中使用的日志系统为slf4j-simple

这样，我们的系统就不得不同时支持并维护logback、log4j、slf4j-simple三种日志框架，非常不便。
解决这个问题的方式就是引入一个适配层，由适配层决定使用哪一种日志系统，而调用端只需要做的事情就是打印日志而不需要关心如何打印日志，slf4j或者commons-logging就是这种适配层。

```java
@Slf4j
public class LoggerTest {
    private final Logger logger = LoggerFactory.getLogger(LoggerTest.class);

    /**
     * 传统方式实现日志
     */
    @Test
    public void test1(){
        logger.debug("debug");//默认日志级别为info
        logger.info("info");
        logger.error("eror");
        logger.warn("warn");
    }

    /**
     * Slf4j注解方式实现日志
     */
    @Test
    public void test2(){
        log.debug("debug");//默认日志级别为info
        log.info("info");
        log.error("error");
        log.warn("warn");
    }

}
```
