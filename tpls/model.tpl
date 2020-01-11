using System;
using DapperExtensions.Mapper;

namespace $solution_name.$project_name.Model.$dir
{
    /// <summary>
    /// 数据库表名: $table_name
    /// 描述: $table_comment 模型层
    /// </summary>
    [Serializable]
    public class $model_name 
    {
        $model_params
    }
     /// <summary>
    /// 数据库表名: $table_name
    /// 描述: $table_comment 字段映射 
    /// </summary>
    public class $model_nameMapper : ClassMapper<$model_name>
    {
        public $model_nameMapper()
        {
            base.Table("$table_name");
            $mapper_params
            AutoMap();
        }
    }

}
