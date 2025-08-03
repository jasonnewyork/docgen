using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using CRMDbOAI.Models;
using CRMDbOAI.Services;

namespace CRMDbOAI.Controllers
{
    public class CustomersController : Controller
    {
        private readonly ICustomerService _service;

        public CustomersController(ICustomerService service)
        {
            _service = service;
        }

        // GET: Customers
        public async Task<IActionResult> Index()
        {
            var customers = await _service.GetAllAsync();
            return View(customers);
        }

        // GET: Customers/Details/5
        public async Task<IActionResult> Details(int id)
        {
            var customer = await _service.GetByIdAsync(id);
            if (customer == null)
                return NotFound();
            return View(customer);
        }

        // GET: Customers/Create
        public IActionResult Create()
        {
            return View();
        }

        // POST: Customers/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("company_name,contact_first_name,contact_last_name,contact_email,address,city,state,country,postal_code,industry")] customer customer)
        {
            if (ModelState.IsValid)
            {
                customer.is_active = true;
                await _service.AddAsync(customer);
                return RedirectToAction(nameof(Index));
            }
            return View(customer);
        }

        // GET: Customers/Edit/5
        public async Task<IActionResult> Edit(int id)
        {
            var customer = await _service.GetByIdAsync(id);
            if (customer == null)
                return NotFound();
            return View(customer);
        }

        // POST: Customers/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("customer_id,company_name,contact_first_name,contact_last_name,contact_email,address,city,state,country,postal_code,industry,is_active")] customer customer)
        {
            if (id != customer.customer_id)
                return NotFound();
            if (ModelState.IsValid)
            {
                await _service.UpdateAsync(customer);
                return RedirectToAction(nameof(Index));
            }
            return View(customer);
        }

        // GET: Customers/Delete/5
        public async Task<IActionResult> Delete(int id)
        {
            var customer = await _service.GetByIdAsync(id);
            if (customer == null)
                return NotFound();
            return View(customer);
        }

        // POST: Customers/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            await _service.DeleteAsync(id);
            return RedirectToAction(nameof(Index));
        }
    }
}
