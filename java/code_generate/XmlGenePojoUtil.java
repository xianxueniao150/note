
@Slf4j
public class XmlGenePojoUtil {
    private static String entityName="KdReturnorderConfirmParam";
    private static String pacName="goods.kd.returnorderConfirm.param";

    public static void main(String[] args) {
        String xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" +
                "<request> \n" +
                "  <returnOrder> \n" +
                "    <returnOrderCode>退货单编码,  string (50) ,  必填</returnOrderCode>  \n" +
                "    <returnOrderId>仓库系统订单编码, string (50) , 条件必填</returnOrderId>  \n" +
                "<warehouseCode>仓库编码, string (50)，必填 </warehouseCode>   \n" +
                "    <orderType>单据类型, string（50）,THRK=退货入库单，HHRK=换货入库 </orderType>  \n" +
                "    <returnReason>退货原因, string (200 </returnReason>  \n" +
                "    <logisticsCode>物流公司编码, string (50) , SF=顺丰、EMS=标准快递、EYB=经济快件、ZJS=宅急送、YTO=圆通  、ZTO=中通 (ZTO) 、HTKY=百世汇通、UC=优速、STO=申通、TTKDEX=天天快递  、QFKD=全峰、FAST=快捷、POSTB=邮政小包  、GTO=国通、YUNDA=韵达、JD=京东配送、DD=当当宅配、AMAZON=亚马逊物流、OTHER=其他， (只传英文编码) </logisticsCode>\n" +
                "    <logisticsName>物流公司名称, string (200) </logisticsName>  \n" +
                "    <expressCode>运单号, string (50) </expressCode>  \n" +
                "<senderInfo> <!--发件人信息-->\n" +
                "  <company>公司名称, string (200) </company>  \n" +
                "      <name>姓名, string (50) </name>  \n" +
                "      <zipCode>邮编, string (50) </zipCode>  \n" +
                "      <tel>固定电话, string (50) </tel>  \n" +
                "      <mobile>移动电话, string (50) </mobile>  \n" +
                "      <email>电子邮箱, string (50) </email>  \n" +
                "      <countryCode>国家二字码，string（50）</countryCode>  \n" +
                "      <province>省份, string (50)  </province>  \n" +
                "      <city>城市, string (50) </city>  \n" +
                "      <area>区域, string (50)  </area>  \n" +
                "      <town>村镇, string (50) </town>  \n" +
                "      <detailAddress>详细地址, string (200) , 必填</detailAddress> \n" +
                "    </senderInfo>  \n" +
                "    <remark>备注, string (500) </remark> \n" +
                "  </returnOrder>  \n" +
                "  <orderLines> \n" +
                "<orderLine> \n" +
                "      <orderLineNo>单据行号，string（50）</orderLineNo>\n" +
                "      <sourceOrderCode>交易平台订单, string (50) </sourceOrderCode>  \n" +
                "      <subSourceOrderCode>交易平台子订单编码, string (50) </subSourceOrderCode>  \n" +
                "      <itemCode>商品编码, string (50) , 必填</itemCode>  \n" +
                "      <itemId>仓储系统商品编码, string (50) , 条件必填</itemId>  \n" +
                "      <inventoryType>库存类型, string (50) , ZP=正品, CC=残次, JS=机损, XS=箱损, 默认为ZP</inventoryType> \n" +
                "<planQty>应收商品数量, int</planQty> \n" +
                "      <actualQty>实收商品数量, int, 必填</actualQty>  \n" +
                "      <batchCode>批次编码, string (50) </batchCode>  \n" +
                "      <productDate>生产日期, string (10) , YYYY-MM-DD</productDate>  \n" +
                "      <expireDate>过期日期, string (10) , YYYY-MM-DD</expireDate>  \n" +
                "    </orderLine> \n" +
                "  </orderLines> \n" +
                "</request>\n";

        try {
            // 创建一个读取器
            SAXReader saxReader = new SAXReader();
            ByteArrayInputStream inputStream = new ByteArrayInputStream(xml.getBytes());
            Document read = saxReader.read(inputStream);
            Element rootElement = read.getRootElement();
            parseElement(rootElement, null);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void parseElement(Element element,List<Map< String, String >> parentFileds) throws IOException {
        String elementName = element.getName();
        if(parentFileds!=null){
            HashMap< String, String > map = new HashMap<>();
            map.put("propertyName", elementName);
            String text = element.getText();
            map.put("comment", text.trim());
            if(element.isTextOnly()){
                if(text.contains("YYYY-MM-DD")){
                    map.put("propertyType", "Date");
                }else if(text.contains("int")){
                    map.put("propertyType", "Integer");
                }else if(text.contains("double")){
                    map.put("propertyType", "BigDecimal");
                } else {
                    map.put("propertyType", "String");
                }
                parentFileds.add(map);
                return;
            }
            map.put("propertyType", StrUtil.upperFirst(elementName));
            parentFileds.add(map);
        }
        HashMap<String, Object> objectMap=new HashMap<>();
        objectMap.put("entityName", StrUtil.upperFirst(elementName));
        if(parentFileds==null){
            objectMap.put("entityName",entityName);
        }
        List<Map< String, String >> fileds=new ArrayList<>();
        for (Element subElement : element.elements()) {
            parseElement(subElement,fileds);
        }
        //处理xml列表
        if(fileds.size()>1 && fileds.get(0).get("propertyName").equals(fileds.get(1).get("propertyName"))){
            Map<String, String> itemMap = fileds.get(0);
            fileds.clear();
            HashMap<String, String> newMap = new HashMap<>();
            newMap.put("propertyName",itemMap.get("propertyName")+"s = new ArrayList<>()");
            newMap.put("propertyType","List<"+itemMap.get("propertyType")+">");
            newMap.put("isList","true");
            newMap.put("listPropertyType",itemMap.get("propertyType"));
            newMap.put("listPropertyName",itemMap.get("propertyName"));
            newMap.put("listMethodName",StrUtil.upperFirst(itemMap.get("propertyName")));
            newMap.put("listPropertyNames",itemMap.get("propertyName")+"s");
            fileds.add(newMap);
        }
        objectMap.put("fields", fileds );
        VelocityUtil.genCode(objectMap,"xmlEntity.vm",pacName);
    }
}

)
