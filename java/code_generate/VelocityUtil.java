@Slf4j
public class VelocityUtil {
    public static void genCode(Map<String, Object> objectMap, String templateName, String pacName) throws IOException {
        objectMap.put("package","com.kbao."+pacName);
        objectMap.put("author","zhaobowen");
        objectMap.put("date", DateUtil.formatDate(new Date()));
        String pac=pacName.replace(".","\\");
        VelocityEngine velocityEngine = new VelocityEngine();
        //设置模板路径，模板和工具类在同一目录下
        velocityEngine.setProperty(Velocity.FILE_RESOURCE_LOADER_PATH, VelocityUtil.class.getResource("").getPath());
        Template template = velocityEngine.getTemplate(templateName);
        String outputDir=new File("").getAbsolutePath()+"\\kbc-asc-shop-entity\\src\\main\\java\\com\\kbao\\"+pac;
       String outputFile = outputDir+"\\" +objectMap.get("entityName")+".java";
        File dir = new File(outputDir);
        if (!dir.exists()) {
            boolean result = dir.mkdirs();
            if (result) {
                log.debug("创建目录： [" + outputDir + "]");
            }
        }
        try (FileOutputStream fos = new FileOutputStream(outputFile);
             OutputStreamWriter ow = new OutputStreamWriter(fos);
             BufferedWriter writer = new BufferedWriter(ow)) {
            template.merge(new VelocityContext(objectMap), writer);
        }
    }
}

 
