## 创建模块文件
 在nginx/src/目录下创建目录ext,在ext目录下以模块名称创建文件ngx_http_hello_world_module.c 其完整结构如下:

```c
#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>

static ngx_int_t ngx_http_hello_world_handler(ngx_http_request_t *r);

ngx_module_t  ngx_http_hello_world_module;

typedef struct {
  
  ngx_str_t header_value;
  
} ngx_http_hello_world_header_loc_conf_t;

static ngx_int_t ngx_http_hello_world_handler(ngx_http_request_t *r){

	printf("%s\n", "-------ngx_http_hello_world_handler--------");
  
  ngx_http_hello_world_header_loc_conf_t* local_conf;
  ngx_table_elt_t  *h;
  //ngx_pool_t *p;

  local_conf = ngx_http_get_module_loc_conf(r,ngx_http_hello_world_module);
  ngx_str_t header_value = local_conf->header_value;

	ngx_int_t rc = ngx_http_discard_request_body(r);
  if (rc != NGX_OK) {
        return rc;
  }

  h = ngx_list_push(&r->eaders_out.headers );
  if(h == NULL){
    	return NGX_ERROR;
  }
  ngx_str_set(&h->key,"X-Hello-World");
  h->value.len = header_value.len;
  h->value.data = header_value.data;
  h->hash = 1;
  
  return NGX_DECLINED;
}

static void *ngx_http_hello_world_create_loc_conf(ngx_conf_t *cf){

  ngx_http_hello_world_header_loc_conf_t* local_conf = NULL;
  local_conf = ngx_pcalloc(cf->pool, sizeof(ngx_http_hello_world_header_loc_conf_t));
  if (local_conf == NULL)
  {
          return NULL;
  }
  ngx_str_null(&local_conf->header_value);

  return local_conf;
}

static char* ngx_http_hello_world_set(ngx_conf_t *cf, ngx_command_t *cmd, void *conf){
	 
   printf("---------ngx_http_hello_world_set--------");
   //ngx_http_hello_world_header_loc_conf_t* local_conf;
   //local_conf = conf;
   char* rv = ngx_conf_set_str_slot(cf, cmd, conf);

    ngx_http_core_loc_conf_t  *clcf;

     clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
     clcf->handler =ngx_http_hello_world_handler;

     return NGX_CONF_OK;
   return rv;

}

static ngx_command_t  ngx_http_hello_world_commands[] = {

  { ngx_string("hello_world_header"),
    NGX_HTTP_LOC_CONF|NGX_CONF_TAKE1,
    ngx_http_hello_world_set,
    NGX_HTTP_LOC_CONF_OFFSET,
    offsetof(ngx_http_hello_world_header_loc_conf_t,header_value),
    NULL },
    ngx_null_command
};


static ngx_http_module_t  ngx_http_hello_world_module_ctx = {
  NULL,                                  /* preconfiguration */
  NULL,             /* postconfiguration */
  NULL,                                  /* create main configuration */
  NULL,                                  /* init main configuration */
  NULL,                                  /* create server configuration */
  NULL,                                  /* merge server configuration */
  ngx_http_hello_world_create_loc_conf,  /* create location configuration */
  NULL                                   /* merge location configuration */
};

ngx_module_t  ngx_http_hello_world_module = {
    NGX_MODULE_V1,
    &ngx_http_hello_world_module_ctx,       /* module context */
    ngx_http_hello_world_commands,          /* module directives */
    NGX_HTTP_MODULE,                       /* module type */
    NULL,                                  /* init master */
    NULL,                                  /* init module */
    NULL,                                  /* init process */
    NULL,                                  /* init thread */
    NULL,                                  /* exit thread */
    NULL,                                  /* exit process */
    NULL,                                  /* exit master */
    NGX_MODULE_V1_PADDING
};
```


## 编写config文件
对于开发一个模块，我们是需要把这个模块的C代码组织到一个目录里，同时需要编写一个config文件。这个config文件的内容就是告诉nginx的编译脚本，该如何进行编译。在ext目录下创建config文件

```
ngx_addon_name=ngx_http_hello_world_module
HTTP_MODULES="$HTTP_MODULES ngx_http_hello_world_module"
NGX_ADDON_SRCS="$NGX_ADDON_SRCS $ngx_addon_dir/ngx_http_hello_world_module.c"
```

## 编译与安装
```
./configure --with-debug --add-module=/home/iknow/nginx/nginx-1.15.1/src/ext/
make
make install
```
执行上述命令进行nginx源码编译与安装,其中xxx为nginx源码的绝对路径。


