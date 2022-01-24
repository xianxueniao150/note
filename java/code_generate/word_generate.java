
@Slf4j
public class AnnotationToPojoUtil {
    private static String entityName="YzhBatchSaleStatusVo";
    private static String packageName ="goods.yzh.vo";
    private static String entityComment ="批量查询商品可售状态";

    public static void main(String[] args) throws IOException {
        String words = "product_id\tint\t商品ID\n" +
                "status\tBoolean\ttrue: 可售,  false:不可售\n" +
                "message\tString\t描述信息\n";
        Map<String, Object> objectMap=new HashMap<>();
        objectMap.put("entityName",entityName);
        objectMap.put("entityComment",entityComment);
        String[] split = words.split("\n");
        List<Map< String, String >> fileds=new ArrayList<>();
        for (String row : split) {
            String[] column =row.split("\t");
            Map< String, String > map = new HashMap<>();
//            String propertyName = CaseFormat.LOWER_UNDERSCORE.to(CaseFormat.LOWER_CAMEL, column[0].trim());
            String propertyName = column[0];
            map.put("propertyName",propertyName.trim());
            String propertyType = column[1];
            String lowProp = propertyType.toLowerCase();
            if("int".equals(lowProp)) {
                propertyType="Integer";
            }
          /*  if("double".equals(lowProp)) {
                propertyType="BigDecimal";
            }*/
            if("必须".equals(lowProp) || "可选".equals(lowProp) || EmptyUtils.isEmpty(lowProp)){
                propertyType="String";
            }
            map.put("propertyType", propertyType);
            map.put("comment",column[2]);
            fileds.add(map);
        }
        objectMap.put("fields", fileds );
        VelocityUtil.genCode(objectMap,"xmlEntity.vm",packageName);
    }
}

 
