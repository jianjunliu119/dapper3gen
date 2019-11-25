using MySql.Data.MySqlClient;
using System.Configuration;
using System.Data;

namespace $solution_name.$project_name.Factory
{
    /// <summary>
    /// Connection工厂用于实例化对应的IDbConnection对象，传递给Dapper。
    /// </summary>
    public class ConnectionFactory
    {
        
        private static readonly string connString = ConfigurationManager.ConnectionStrings["constr"].ConnectionString;
        //生成连接数据库字符串添加到配置文件即可
        //"server = $host;User Id = $user;password = $password;Database = $db"

        public static IDbConnection CreateConnection()
        {
            IDbConnection conn = null;
            conn = new MySqlConnection(connString);
            conn.Open();
            return conn;
        }

    }
}
