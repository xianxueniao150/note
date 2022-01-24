
public class FileUtils {

    //查询某个目录下的所有文件，配合下面searchFiles一起使用
    public static List<File> searchAllFile(File dir) throws IOException {
        List<File> arrayList = new ArrayList<>();
        searchFiles(dir,arrayList);
        return arrayList;
    }

    //递归获取某个目录下的所有文件
    private static void searchFiles(File dir,List<File> collector) throws IOException {
        if(dir.isDirectory()) {
            File[] subFiles = dir.listFiles();
            for(int i = 0; i < subFiles.length; i++) {
                searchFiles(subFiles[i],collector);
            }
        }else{
            collector.add(dir);
        }
    }
    
    /**
     *创建文件夹,会生成file中表示文件夹的部分
     * @param dir  C:\Users\fengyin\Documents\生成代码
     * @param file   aaa\eee\index.htl
     * @return
     */
    public static File mkdir(String dir,String file) {
        if(dir == null) throw new IllegalArgumentException("dir must be not null");
        File result = new File(dir,file);
        if(result.getParentFile() != null) {
            //mkdir()和mkdirs()的区别是如果新建的文件目录的上级目录不存在则mkdir()会报异常不能成功创建文件夹，而mkdirs()会将目录与上级目录一起创建。
            result.getParentFile().mkdirs();
        }
        return result;
    }
}

m
