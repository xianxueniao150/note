duboo默认日志框架
需在资源文件夹中新建Log4j.properties
```sh
log4j.rootLogger=INFO,console
# 控制台(console)
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.Threshold=DEBUG
log4j.appender.console.ImmediateFlush=true
log4j.appender.console.layout=org.apache.log4j.PatternLayout
# 如果希望输出默认时间格式，即到ms，就删除{yyyy/MM/dd HH:mm:ss}
log4j.appender.console.layout.ConversionPattern=[%-5p] %d{yyyy/MM/dd HH:mm:ss} --> [%t] %l: %m %x %n
```



