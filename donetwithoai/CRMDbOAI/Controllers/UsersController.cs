using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using CRMDbOAI.Models;
using CRMDbOAI.Services;

namespace CRMDbOAI.Controllers
{
    public class UsersController : Controller
    {
        private readonly IUserService _service;
        private readonly IRoleService _roleService;
        public UsersController(IUserService service, IRoleService roleService)
        {
            _service = service;
            _roleService = roleService;
        }

        public async Task<IActionResult> Index()
        {
            var users = await _service.GetAllAsync();
            return View(users);
        }

        public async Task<IActionResult> Details(int id)
        {
            var user = await _service.GetByIdAsync(id);
            if (user == null) return NotFound();
            return View(user);
        }

        public async Task<IActionResult> Create()
        {
            var roles = await _roleService.GetAllAsync();
            ViewBag.Roles = new Microsoft.AspNetCore.Mvc.Rendering.SelectList(roles, "role_id", "role_name");
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("username,email,first_name,last_name,password_hash,role_id,is_active")] user user)
        {
            if (ModelState.IsValid)
            {
                user.is_active = true;
                await _service.AddAsync(user);
                return RedirectToAction(nameof(Index));
            }
            var roles = await _roleService.GetAllAsync();
            ViewBag.Roles = new Microsoft.AspNetCore.Mvc.Rendering.SelectList(roles, "role_id", "role_name", user.role_id);
            return View(user);
        }

        public async Task<IActionResult> Edit(int id)
        {
            var user = await _service.GetByIdAsync(id);
            if (user == null) return NotFound();
            var roles = await _roleService.GetAllAsync();
            ViewBag.Roles = new Microsoft.AspNetCore.Mvc.Rendering.SelectList(roles, "role_id", "role_name", user.role_id);
            return View(user);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("user_id,username,email,first_name,last_name,password_hash,role_id,is_active")] user user)
        {
            if (id != user.user_id) return NotFound();
            if (ModelState.IsValid)
            {
                await _service.UpdateAsync(user);
                return RedirectToAction(nameof(Index));
            }
            var roles = await _roleService.GetAllAsync();
            ViewBag.Roles = new Microsoft.AspNetCore.Mvc.Rendering.SelectList(roles, "role_id", "role_name", user.role_id);
            return View(user);
        }

        public async Task<IActionResult> Delete(int id)
        {
            var user = await _service.GetByIdAsync(id);
            if (user == null) return NotFound();
            return View(user);
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
