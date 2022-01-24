public class BeanUtil {
    public static Map<String, String> beanToMap(Object object) {
        HashMap<String, String> map = JSON.parseObject(JSON.toJSONString(object), new TypeReference<HashMap<String, String>>() {
        });
        return map;
    }

    public static <S, T> List<T> copyListProperties(List<S> sources, Supplier<T> supplier) {
        return copyListProperties(sources, supplier, null);
    }

    public static <S, T> List<T> copyListProperties(List<S> sources, Supplier<T> supplier, BiConsumer<S, T> biConsumer) {
        List<T> list = new ArrayList<>(sources.size());
        sources.forEach(s -> {
            T t = supplier.get();
            BeanUtils.copyProperties(s, t);
            if (biConsumer != null) {
                bionsumer.accept(s, t);
            }
            list.add(t);
        });
        return list;
    }
}

C
