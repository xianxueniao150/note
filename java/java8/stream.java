
/* Stream API 的操作步骤：
 * 1. 创建 Stream
 * 2. 中间操作
 * 3. 终止操作(终端操作)
 */


1. 创建 Stream
//1. Collection 提供了两个方法  stream() 与 parallelStream()
List<String> list = new ArrayList<>();
Stream<String> stream = list.stream(); //获取一个顺序流
Stream<String> parallelStream = list.parallelStream(); //获取一个并行流

//2. 通过 Arrays 中的 stream() 获取一个数组流
Integer[] nums = new Integer[10];
Stream<Integer> stream1 = Arrays.stream(nums);

//3. 通过 Stream 类中静态方法 of()
Stream<Integer> stream2 = Stream.of(1,2,3,4,5,6);

//4. 创建无限流
//迭代
Stream<Integer> stream3 = Stream.iterate(0, (x) -> x + 2).limit(10);
stream3.forEach(System.out::println);

//生成
Stream<Double> stream4 = Stream.generate(Math::random).limit(2);
stream4.forEach(System.out::println);


2. 中间操作
/*
  筛选与切片
   filter——接收 Lambda  从流中排除某些元素。
   limit——截断流，使其元素不超过给定数量。
   skip(n) —— 跳过元素，返回一个扔掉了前 n 个元素的流。若流中元素不足 n 个，则返回一个空流。与 limit(n) 互补
   distinct——筛选，通过流所生成元素的 hashCode() 和 equals() 去除重复元素
 */
 
 emps.parallelStream()
   .filter((e) -> e.getSalary() >= 5000)
   .skip(2)
   .forEach(System.out::println);
   
/*
映射
map——接收 Lambda ， 将元素转换成其他形式或提取信息。接收一个函数作为参数，该函数会被应用到每个元素上，并将其映射成一个新的元素。
flatMap——接收一个函数作为参数，将流中的每个值都换成另一个流，然后把所有流连接成一个流
*/
strList.stream()
      .map(String::toUpperCase)
emps.stream()
   .map(Employee::getName)
   
   
/*
sorted()——自然排序
sorted(Comparator com)——定制排序
*/
emps.stream()
   .sorted((x, y) -> {
      if(x.getAge() == y.getAge()){
         return x.getName().compareTo(y.getName());
      }else{
         return Integer.compare(x.getAge(), y.getAge());
      }
   }).forEach(System.out::println);



3. 终止操作
/*
   allMatch——检查是否匹配所有元素
   anyMatch——检查是否至少匹配一个元素
   noneMatch——检查是否没有匹配的元素
   findFirst——返回第一个元素
   findAny——返回当前流中的任意元素
   count——返回流中元素的总个数
   max——返回流中最大值
   min——返回流中最小值
 */
 
boolean bl = emps.stream()
   .allMatch((e) -> e.getStatus().equals(Status.BUSY));
   
Optional<Employee> op = emps.stream()
        .sorted(Comparator.comparingDouble(Employee::getSalary))
        .findFirst();
Employee employee = op.get();

