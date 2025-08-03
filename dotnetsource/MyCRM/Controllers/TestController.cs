using Microsoft.AspNetCore.Mvc;

namespace MyCRM.Controllers
{
    public class TestController : Controller
    {
        public IActionResult Index()
        {
            return Content("Test controller works! This means routing is fine.");
        }
        
        public IActionResult Customers()
        {
            return Content("Test customers action works! The issue is with the real CustomerController.");
        }
    }
}
