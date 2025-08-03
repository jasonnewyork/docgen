using Microsoft.AspNetCore.Mvc;

namespace MyCRM.Controllers
{
    public class SimpleHomeController : Controller
    {
        public IActionResult Index()
        {
            ViewBag.Message = "MyCRM Application is Running!";
            ViewBag.Time = DateTime.Now.ToString("F");
            return View();
        }
        
        public IActionResult About()
        {
            ViewBag.Message = "This is a Customer Relationship Management System";
            return View();
        }
    }
}
