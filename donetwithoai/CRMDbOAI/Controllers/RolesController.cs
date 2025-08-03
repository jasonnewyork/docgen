using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using CRMDbOAI.Models;
using CRMDbOAI.Services;

namespace CRMDbOAI.Controllers
{
    public class RolesController : Controller
    {
        private readonly IRoleService _service;
        public RolesController(IRoleService service) => _service = service;

        public async Task<IActionResult> Index()
        {
            var roles = await _service.GetAllAsync();
            return View(roles);
        }

        public async Task<IActionResult> Details(int id)
        {
            var role = await _service.GetByIdAsync(id);
            if (role == null) return NotFound();
            return View(role);
        }

        public IActionResult Create() => View();

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("role_name,description")] role role)
        {
            if (ModelState.IsValid)
            {
                await _service.AddAsync(role);
                return RedirectToAction(nameof(Index));
            }
            return View(role);
        }

        public async Task<IActionResult> Edit(int id)
        {
            var role = await _service.GetByIdAsync(id);
            if (role == null) return NotFound();
            return View(role);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("role_id,role_name,description") ] role role)
        {
            if (id != role.role_id) return NotFound();
            if (ModelState.IsValid)
            {
                await _service.UpdateAsync(role);
                return RedirectToAction(nameof(Index));
            }
            return View(role);
        }

        public async Task<IActionResult> Delete(int id)
        {
            var role = await _service.GetByIdAsync(id);
            if (role == null) return NotFound();
            return View(role);
        }

        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            await _service.DeleteAsync(id);
            return RedirectToAction(nameof(Index));
        }
    }
}
