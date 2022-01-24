简单项目日志
```sh
<!-- SLF4J -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-log4j12</artifactId>
    <version>1.7.7</version>
</dependency>
```


```sh
log4j.properties
log4j.rootLogger=ERROR,console,file

log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%m%n

log4j.appender.file=org.apache.log4j.DailyRollingFileAppender
log4j.appender.file.File=${user.home}/logs/book.log
log4j.appender.file.DatePattern='_'yyyyMMdd
log4j.appender.file.layout=org.apache.log4j.PatternLayout
log4j.appender.file.layout.ConversionPattern=%d{HH:mm:ss,SSS} %p %c (%L) - %m%n

log4j.logger.com.bowen.mybatis=DEBUG
```


```java
@Slf4j
```


```java
log.debug("statement:{}", statement;

)
```
