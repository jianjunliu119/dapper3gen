using System.Collections.Generic;

namespace $solution_name.Common
{
    public class PageData<T> :List<T>
    {
        public int PageIndex { get; set; }
        public int PageSize { get; set; }
        public int TotalCount { get; set; }
        public IList<T> Data { get; set; }
    }
}
