using Dapper;
using $solution_name.Common;
using $solution_name.$project_name.Factory;
using $solution_name.$project_name.Model.$dir;
using System.Collections.Generic;
using System.Data;
using System.Linq;

namespace $solution_name.$project_name.DAL.$dir
{
    /// <summary>
    /// 数据库表名: $table_name
    /// 描述: $table_comment 数据访问层 
    /// </summary>
    public class $model_nameDAL
    {
        private IDbConnection _conn;

        public IDbConnection Conn
        {
            get
            {
                Dapper.DefaultTypeMap.MatchNamesWithUnderscores = true;
                return _conn = ConnectionFactory.CreateConnection();
            }
        }
        #region CURD

        public int Insert($model_name $model_name_low)
        {
            using (Conn)
            {
                return Conn.Execute(@"$insert_sql", $model_name_low);
            }
        }
        public int Update($model_name $model_name_low)
        {
            using (Conn)
            {
                return Conn.Execute(@"$update_sql", $model_name_low);
            }
        }

        public int Delete($model_name $model_name_low)
        {
            using (Conn)
            {
                return Conn.Execute(@"delete from $table_name where id = @id", $model_name_low);
            }
        }

        public int Delete(string id)
        {
            using (Conn)
            {
                return Conn.Execute(@"delete from $table_name where id = @id", new { Id = id });
            }
        }
        public $model_name GetOne(string id)
        {
            using (Conn)
            {
                string sql = "select * from $table_name where id = @id";
                return Conn.Query<$model_name>(sql, new { Id = id }).SingleOrDefault();
            }
        }
        public IList<$model_name> GetAll()
        {
            using (Conn)
            {
                string sql = "select * from $table_name order by create_time desc";
                return Conn.Query<$model_name>(sql).ToList();
            }
        }
        /// <summary>
        /// 分页
        /// </summary>
        /// <param name="pageIndex"></param>
        /// <param name="pageSize"></param>
        /// <returns></returns>
        public PageData<$model_name> GetAll(int pageIndex, int pageSize)
        {
            PageData<$model_name> pd = new PageData<$model_name>()
            {
                PageIndex = pageIndex,
                PageSize = pageSize
            };
            using (Conn)
            {
                string sql = "select * from $table_name where 1=1 ";
                // 查询条件
                sql +=" order by create_time desc";
                pd.TotalCount = Conn.Query<$model_name>(sql).Count();
                //pd.TotalPage = (pd.TotalCount + pageSize - 1) / pageSize;
                string pageSql = sql + " limit " + (pageIndex - 1) * pageSize + "," + pageSize;
                pd.Data = Conn.Query<$model_name>(pageSql).ToList();
            }
            return pd;
        }
        #endregion
    }
}
