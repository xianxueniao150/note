## 一、Lambda 表达式需要“函数式接口”的支持
函数式接口：接口中只有一个抽象方法的接口，称为函数式接口。
         	可以使用注解 @FunctionalInterface 修饰,会检查是否是函数式接口

## 二、Lambda 表达式的基础语法：
Java8中引入了一个新的操作符 "->" 该操作符将 Lambda 表达式拆分成两部分：
左侧：Lambda 表达式的参数列表
右侧：Lambda 表达式中所需执行的功能， 即 Lambda 体
语法格式一：无参数，无返回值
     () -> System.out.println("Hello Lambda!");

语法格式二：有一个参数，并且无返回值，若只有一个参数，小括号可以省略不写
     (x) -> System.out.println(x)

语法格式四：有两个以上的参数，有返回值，并且 Lambda 体中有多条语句
      Comparator<Integer> com = (x, y) -> {
   System.out.println("函数式接口");
   return Integer.compare(x, y);
};

语法格式五：若 Lambda 体中只有一条语句， return 和 大号都可以省略不写
     Comparator<Integer> com = (x, y) -> Integer.compare(x, y);

语法格式六：Lambda 表达式的参数列表的数据类型可以省略不写，因为JVM编译器通过上下文推断出，数据类型
      (Integer x, Integer y) -> Integer.compare(x, y);

```java
//1.首先申明函数式接口
public interface MyFun {
   public Integer getValue(Integer num);  
}

//2.申明方法
public Integer operation(Integer num, MyFun mf){
   return mf.getValue(num);
}

//3.使用
Integer num = operation(100, (x) -> x * x);
Integer num2 = operation(200, (y) -> y + 200);

or
@FunctionalInterface
interface Converter<F, T> {
    T convert(F from);
}

Converter<String, Integer> converter = (from) -> Integer.valueOf(from);
Integer converted = converter.convert("123");
System.out.println(converted);    // 123



Java8 内置的四大核心函数式接口

/*
 * Java8 内置的四大核心函数式接口
 * 
 * Consumer<T> : 消费型接口
 *        void accept(T t);
 * 
 * Supplier<T> : 供给型接口
 *        T get(); 
 * 
 * Function<T, R> : 函数型接口
 *        R apply(T t);
 * 
 * Predicate<T> : 断言型接口
 *        boolean test(T t);
 * 
 */
public class TestLambda3 {
   
   //Predicate<T> 断言型接口：
   @Test
   public void test4(){
      List<String> list = Arrays.asList("Hello", "atguigu", "Lambda", "www", "ok");
      List<String> strList = filterStr(list, (s) -> s.length() > 3);
      
      for (String str : strList) {
         System.out.println(str);
      }
   }
   
   //需求：将满足条件的字符串，放入集合中
   public List<String> filterStr(List<String> list, Predicate<String> pre){
      List<String> strList = new ArrayList<>();
      
      for (String str : list) {
         if(pre.test(str)){
            strList.add(str);
         }
      }
      return strList;
   }
   
   //Function<T, R> 函数型接口：
   @Test
   public void test3(){
      String newStr = strHandler("\t\t\t 我大尚硅谷威武   ", (str) -> str.trim());
      System.out.println(newStr);
      
      String subStr = strHandler("我大尚硅谷威武", (str) -> str.substring(2, 5));
      System.out.println(subStr);
   }
   
   //需求：用于处理字符串
   public String strHandler(String str, Function<String, String> fun){
      return fun.apply(str);
   }
   
   //Supplier<T> 供给型接口 :
   @Test
   public void test2(){
      List<Integer> numList = getNumList(10, () -> (int)(Math.random() * 100));
      
      for (Integer num : numList) {
         System.out.println(num);
      }
   }
   
   //需求：产生指定个数的整数，并放入集合中
   public List<Integer> getNumList(int num, Supplier<Integer> sup){
      List<Integer> list = new ArrayList<>();
      
      for (int i = 0; i < num; i++) {
         Integer n = sup.get();
         list.add(n);
      }
      
      return list;
   }
   
   //Consumer<T> 消费型接口 :
   @Test
   public void test1(){
      happy(10000, (m) -> System.out.println("你们刚哥喜欢大宝剑，每次消费：" + m + "元"));
   } 
   
   public void happy(double money, Consumer<Double> con){
      con.accept(money);
   }
}

```
