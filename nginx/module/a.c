定义HTTP模块方式很简单，例如：

ngx_module_t ngx_http_mytest_module;
其中，ngx_module_t 是一个Nginx模块的数据结构（详见8.2节）。下面来分析一下Nginx模块中所有的成员，如下所示：

typedef struct ngx_module_s      ngx_module_t;
struct ngx_module_s {
 /* 下面的ctx_index、index、spare0、spare1、spare2、spare3、version变量不需要在定义时赋值，可以用Nginx准备好的宏NGX_MODULE_V1来定义，它已经定义好了这7个值。
#define NGX_MODULE_V1          0, 0, 0, 0, 0, 0, 1
对于一类模块（由下面的type成员决定类别）而言，ctx_index表示当前模块在这类模块中的序号。这个成员常常是由管理这类模块的一个Nginx核心模块设置的，对于所有的HTTP模块而言，ctx_index是由核心模块ngx_http_module设置的。ctx_index非常重要，Nginx的模块化设计非常依赖于各个模块的顺序，它们既用于表达优先级，也用于表明每个模块的位置，借以帮助Ngnx框架快速获得某个模块的数据（HTTP框架设置ctx_index的过程参见10.7节）*/
ngx_uint_t            ctx_index;
/*index表示当前模块在ngx_modules数组中的序号。注意，ctx_index表示的是当前模块在一类模块中的序号，而index表示当前模块在所有模块中的序号，它同样关键。Nginx启动时会根据ngx_modules数组设置各模块的index值。例如：
ngx_max_module = 0;
for (i = 0; ngx_modules[i]; i++) {
   ngx_modules[i]->index = ngx_max_module++;
}
*/
   ngx_uint_t            index;

   //spare系列的保留变量，暂未使用
   ngx_uint_t            spare0;
   ngx_uint_t            spare1;
   ngx_uint_t            spare2;
   ngx_uint_t            spare3;
   //模块的版本，便于将来的扩展。目前只有一种，默认为1
   ngx_uint_t            version;

   /*ctx用于指向一类模块的上下文结构体，为什么需要ctx呢？因为前面说过，Nginx模块有许多种类，不同类模块之间的功能差别很大。例如，事件类型的模块主要处理I/O事件相关的功能，HTTP类型的模块主要处理HTTP应用层的功能。这样，每个模块都有了自己的特性，而ctx将会指向特定类型模块的公共接口。例如，在HTTP模块中，ctx需要指向ngx_http_module_t结构体*/
   void                 *ctx;

   //commands将处理nginx.conf中的配置项，详见第4章
   ngx_command_t        *commands;

   /*type表示该模块的类型，它与ctx指针是紧密相关的。在官方Nginx中，它的取值范围是以下5种：NGX_HTTP_MODULE、NGX_CORE_MODULE、NGX_CONF_MODULE、NGX_EVENT_MODULE、NGX_MAIL_MODULE。这5种模块间的关系参考图8-2。实际上，还可以自定义新的模块类型*/
   ngx_uint_t            type;

   /*在Nginx的启动、停止过程中，以下7个函数指针表示有7个执行点会分别调用这7种方法（参见8.4节～8.6节）。对于任一个方法而言，如果不需要Nginx在某个时刻执行它，那么简单地把它设为NULL空指针即可*/

   /*虽然从字面上理解应当在master进程启动时回调init_master，但到目前为止，框架代码从来不会调用它，因此，可将init_master设为NULL */
   ngx_int_t           (*init_master)(ngx_log_t *log);
   /*init_module回调方法在初始化所有模块时被调用。在master/worker模式下，这个阶段将在启动worker子进程前完成*/
   ngx_int_t           (*init_module)(ngx_cycle_t *cycle);
/* init_process回调方法在正常服务前被调用。在master/worker模式下，多个worker子进程已经产生，在每个worker进程的初始化过程会调用所有模块的init_process函数*/
   ngx_int_t           (*init_process)(ngx_cycle_t *cycle);
/* 由于Nginx暂不支持多线程模式，所以init_thread在框架代码中没有被调用过，设为NULL*/
   ngx_int_t           (*init_thread)(ngx_cycle_t *cycle);
// 同上，exit_thread也不支持，设为NULL
   void                (*exit_thread)(ngx_cycle_t *cycle);
/* exit_process回调方法在服务停止前调用。在master/worker模式下，worker进程会在退出前调用它*/
   void                (*exit_process)(ngx_cycle_t *cycle);
// exit_master回调方法将在master进程退出前被调用
   void                (*exit_master)(ngx_cycle_t *cycle);

   /*以下8个spare_hook变量也是保留字段，目前没有使用，但可用Nginx提供的NGX_MODULE_V1_PADDING宏来填充。看一下该宏的定义：#define NGX_MODULE_V1_PADDING  0, 0, 0, 0, 0, 0, 0, 0*/
   uintptr_t             spare_hook0;
   uintptr_t             spare_hook1;
   uintptr_t             spare_hook2;
   uintptr_t             spare_hook3;
   uintptr_t             spare_hook4;
   uintptr_t             spare_hook5;
   uintptr_t             spare_hook6;
   uintptr_t             spare_hook7;
};
定义一个HTTP模块时，务必把type字段设为NGX_HTTP_MODULE。
对于下列回调方法：init_module、init_process、exit_process、exit_master，调用它们的是Nginx的框架代码。换句话说，这4个回调方法与HTTP框架无关，即使nginx.conf中没有配置http {...}这种开启HTTP功能的配置项，这些回调方法仍然会被调用。因此，通常开发HTTP模块时都把它们设为NULL空指针。这样，当Nginx不作为Web服务器使用时，不会执行HTTP模块的任何代码。
定义HTTP模块时，最重要的是要设置ctx和commands这两个成员。对于HTTP类型的模块来说，ngx_module_t中的ctx指针必须指向ngx_http_module_t接口（HTTP框架的要求）。下面先来分析ngx_http_module_t结构体的成员。
HTTP框架在读取、重载配置文件时定义了由ngx_http_module_t接口描述的8个阶段，HTTP框架在启动过程中会在每个阶段中调用ngx_http_module_t中相应的方法。当然，如果ngx_http_module_t中的某个回调方法设为NULL空指针，那么HTTP框架是不会调用它的。

typedef struct {
    //解析配置文件前调用
    ngx_int_t   (*preconfiguration)(ngx_conf_t *cf);
    //完成配置文件的解析后调用
    ngx_int_t   (*postconfiguration)(ngx_conf_t *cf);

    /*当需要创建数据结构用于存储main级别（直属于http{...}块的配置项）的全局配置项时，可以通过create_main_conf回调方法创建存储全局配置项的结构体*/
    void       *(*create_main_conf)(ngx_conf_t *cf);
    //常用于初始化main级别配置项
    char       *(*init_main_conf)(ngx_conf_t *cf, void *conf);

    /*当需要创建数据结构用于存储srv级别（直属于虚拟主机server{...}块的配置项）的配置项时，可以通过实现create_srv_conf回调方法创建存储srv级别配置项的结构体*/
    void       *(*create_srv_conf)(ngx_conf_t *cf);
    // merge_srv_conf回调方法主要用于合并main级别和srv级别下的同名配置项
    char       *(*merge_srv_conf)(ngx_conf_t *cf, void *prev, void *conf);

    /*当需要创建数据结构用于存储loc级别（直属于location{...}块的配置项）的配置项时，可以实现create_loc_conf回调方法*/
    void       *(*create_loc_conf)(ngx_conf_t *cf);
    // merge_loc_conf回调方法主要用于合并srv级别和loc级别下的同名配置项
    char       *(*merge_loc_conf)(ngx_conf_t *cf, void *prev, void *conf);
} ngx_http_module_t;
不过，这8个阶段的调用顺序与上述定义的顺序是不同的。在Nginx启动过程中，HTTP框架调用这些回调方法的实际顺序有可能是这样的（与nginx.conf配置项有关）：

1）create_main_conf
2）create_srv_conf
3）create_loc_conf
4）preconfiguration
5）init_main_conf
6）merge_srv_conf
7）merge_loc_conf
8）postconfiguration
commands数组用于定义模块的配置文件参数，每一个数组元素都是ngx_command_t类型，数组的结尾用ngx_null_command表示。Nginx在解析配置文件中的一个配置项时首先会遍历所有的模块，对于每一个模块而言，即通过遍历commands数组进行，另外，在数组中检查到ngx_null_command时，会停止使用当前模块解析该配置项。每一个ngx_command_t结构体定义了自己感兴趣的一个配置项：

typedef struct ngx_command_s     ngx_command_t;
struct ngx_command_s {
    //配置项名称，如"gzip"
    ngx_str_t             name;
    /*配置项类型，type将指定配置项可以出现的位置。例如，出现在server{}或location{}中，以及它可以携带的参数个数*/
    ngx_uint_t            type;
    //出现了name中指定的配置项后，将会调用set方法处理配置项的参数
    char               *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
    //在配置文件中的偏移量
    ngx_uint_t            conf;
    /*通常用于使用预设的解析方法解析配置项，这是配置模块的一个优秀设计。它需要与conf配合使用，在第4章中详细介绍*/
    ngx_uint_t            offset;
    //配置项读取后的处理方法，必须是ngx_conf_post_t结构的指针
    void                 *post;
};
ngx_null_command只是一个空的ngx_command_t，如下所示：
#define ngx_null_command  { ngx_null_string, 0, NULL, 0, 0, NULL }i
