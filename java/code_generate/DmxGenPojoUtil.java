
public class DmxGenPojoUtil {
    private static String entityName="GoodsSelfEntryOrder";
    private static String packageName ="goods.yzh.param";
    private static String entityComment ="单个查询商品库存";

    public static void main(String[] args) throws IOException {
        String words = "GoodsSelf(自营商品表)\n" +
                "----------------------------------------------------\n" +
                "id(主键)                              FKString(100)\n" +
                "goodsCode(商品编号)                   String\n" +
                "wmsGoodsId(WMS商品编号)               String(100)\n" +
                "barCode(条形码)                       String(100)\n" +
                "goodsSelfSupplierId(供货商编号)       FKString\n" +
                "name(商品名称)                       String(200)\n" +
                "costPrice(成本价格)                   String\n" +
                "unit(计量单位)                        String(20)\n" +
                "taxRate(商品税率)                     Float\n" +
                "length(长度)                          Float\n" +
                "width(宽度)                           Float\n" +
                "height(高度)                          Float\n" +
                "volume(体积)                          Float\n" +
                "grossWeight(毛重)                     Float\n" +
                "netWeight(净重)                       Float\n" +
                "createId(创建人)                      String(100)\n" +
                "createTime(创建时间)                  Date\n" +
                "updateId(更新人)                      String(100)\n" +
                "updateTime(更新时间)                  Date\n" +
                "isDeleted(是否删除)                   Integer(1)  //0 未删除  1已删除\n" +
                "stock(库存)                           Integer\n" +
                "lockStock(冻结库存)                   Integer\n" +
                "zpStock(正品库存)                     Integer\n" +
                "ccStock(残次库存)                     Integer\n" +
                "jsStock(机损库存)                     Integer\n" +
                "xzStock(箱损库存)                     Integer\n" +
                "ztStock(在途库存)                     Integer\n" +
                "goodsSelfSalesList(商品销售情况集合)  List\n";
        Map<String, Object> objectMap=new HashMap<>();
        objectMap.put("entityName",entityName);
        objectMap.put("entityComment",entityComment);
        String[] split = words.split("\n");
        List<Map< String, String >> fileds=new ArrayList<>();
        for (int i = 0; i < split.length; i++) {
            String row =split[i];
            if(i==0){
                String entityName=row.split("\\(")[0];
                continue;
            }
            if(i==1){
                continue;
            }
            Map< String, String > map = new HashMap<>();
            map.put("propertyName",row.split("\\(")[0]);
            map.put("comment",row.substring(row.indexOf("(")+1,row.indexOf(")")));
            String propertyType = row.substring(row.indexOf(")")+1).trim();
            if(propertyType.contains("(")){
                propertyType=propertyType.split("\\(")[0];
            }
            if("FKString".equals(propertyType) /*|| "boolean".equals(lowProp)*/) {
                propertyType="String";
            }
            if("double".equals(propertyType)) {
                propertyType="BigDecimal";
            }
            map.put("propertyType", propertyType);
            fileds.add(map);
        }
        objectMap.put("fields", fileds );
//        VelocityUtil.genCode(objectMap,"xmlEntity.vm",packageName);
    }
}

 
