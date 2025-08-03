using Microsoft.AspNetCore.Mvc;

namespace MyCRM.Controllers
{
    public class CustomerController : Controller
    {
        public IActionResult Index()
        {
            ViewBag.Title = "Customer Management";
            ViewBag.Message = "Customers"; 
            return View("~/Views/Home/Index.cshtml");
        }
    }
}
