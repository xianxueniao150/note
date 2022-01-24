
package ${package};

import java.util.Date;
import java.util.List;
import java.util.ArrayList;
import java.math.BigDecimal;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import lombok.experimental.Accessors;
import java.io.Serializable;

/**
 * @author ${author}
 * @since ${date}
 * @description:$!{entityComment}
 */
@Data
@Accessors(chain = true)
public class ${entityName} implements Serializable {

    private static final long serialVersionUID = 1L;

## ----------  BEGIN 字段循环遍历  ----------
#foreach($field in ${fields})

    /**
     * $!{field.comment}
     */
    private ${field.propertyType} ${field.propertyName};
#end
#foreach($field in ${fields})
    #if(${field.isList})
    public void add${field.listMethodName}(${fild.listPropertyType} ${field.listPropertyName}){
        ${field.listPropertyNames}.add(${field.listPropertyName});
    }
    #end
#end
}

