using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using MyCRM.Models;
using MyCRM.Models.DTOs;
using MyCRM.Repositories;

namespace MyCRM.Services
{
    public interface IAuthService
    {
        Task<LoginResultDto> LoginAsync(LoginDto loginDto);
        Task<UserDto?> GetCurrentUserAsync(ClaimsPrincipal user);
        Task<string> GenerateJwtTokenAsync(User user);
        Task<bool> ChangePasswordAsync(int userId, ChangePasswordDto changePasswordDto);
        Task<bool> LogoutAsync(string userId);
    }

    public class AuthService : IAuthService
    {
        private readonly IUserRepository _userRepository;
        private readonly IConfiguration _configuration;
        private readonly ILogger<AuthService> _logger;

        public AuthService(
            IUserRepository userRepository,
            IConfiguration configuration,
            ILogger<AuthService> logger)
        {
            _userRepository = userRepository;
            _configuration = configuration;
            _logger = logger;
        }

        public async Task<LoginResultDto> LoginAsync(LoginDto loginDto)
        {
            try
            {
                var user = await _userRepository.GetByUsernameAsync(loginDto.Username);
                if (user == null)
                {
                    _logger.LogWarning("Login attempt with non-existent username: {Username}", loginDto.Username);
                    return new LoginResultDto 
                    { 
                        Success = false,
                        ErrorMessage = "Invalid username or password."
                    };
                }

                // Check if account is locked
                if (user.IsLockedOut)
                {
                    _logger.LogWarning("Login attempt for locked account: {Username}", loginDto.Username);
                    return new LoginResultDto 
                    { 
                        Success = false,
                        ErrorMessage = "Account is temporarily locked. Please try again later."
                    };
                }

                // Verify password
                if (!BCrypt.Net.BCrypt.Verify(loginDto.Password, user.PasswordHash))
                {
                    await _userRepository.IncrementFailedLoginAttemptsAsync(user.Id);
                    
                    // Lock account after max attempts
                    var maxAttempts = _configuration.GetValue<int>("Security:MaxLoginAttempts", 5);
                    if (user.FailedLoginAttempts + 1 >= maxAttempts)
                    {
                        await _userRepository.SetLockoutAsync(user.Id, DateTime.UtcNow.AddMinutes(30));
                        _logger.LogWarning("Account locked for user: {Username} after {Attempts} failed attempts", 
                            loginDto.Username, user.FailedLoginAttempts + 1);
                    }

                    _logger.LogWarning("Failed login attempt for user: {Username}", loginDto.Username);
                    return new LoginResultDto 
                    { 
                        Success = false,
                        ErrorMessage = "Invalid username or password."
                    };
                }

                // Successful login
                await _userRepository.ResetFailedLoginAttemptsAsync(user.Id);
                await _userRepository.UpdateLastLoginAsync(user.Id);

                var token = GenerateJwtToken(user);
                var userDto = MapToUserDto(user);

                _logger.LogInformation("User {Username} logged in successfully", loginDto.Username);
                return new LoginResultDto 
                { 
                    Success = true,
                    Token = token,
                    User = userDto,
                    ExpiresAt = DateTime.UtcNow.AddHours(24)
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during login for user: {Username}", loginDto.Username);
                return new LoginResultDto 
                { 
                    Success = false,
                    ErrorMessage = "An error occurred during login. Please try again."
                };
            }
        }

        public async Task<UserDto?> GetCurrentUserAsync(ClaimsPrincipal userPrincipal)
        {
            var userIdClaim = userPrincipal.FindFirst(ClaimTypes.NameIdentifier);
            if (userIdClaim == null || !int.TryParse(userIdClaim.Value, out var userId))
            {
                return null;
            }

            var user = await _userRepository.GetByIdAsync(userId);
            return user != null ? MapToUserDto(user) : null;
        }

        public Task<string> GenerateJwtTokenAsync(User user)
        {
            return Task.FromResult(GenerateJwtToken(user));
        }

        private string GenerateJwtToken(User user)
        {
            var jwtSecretKey = _configuration["JWT:SecretKey"] 
                ?? throw new InvalidOperationException("JWT secret key not configured");

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSecretKey));
            var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var claims = new[]
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.Username),
                new Claim(ClaimTypes.Email, user.Email),
                new Claim(ClaimTypes.GivenName, user.FirstName ?? string.Empty),
                new Claim(ClaimTypes.Surname, user.LastName ?? string.Empty),
                new Claim(ClaimTypes.Role, user.Role.RoleName)
            };

            var token = new JwtSecurityToken(
                issuer: _configuration["JWT:Issuer"],
                audience: _configuration["JWT:Audience"],
                claims: claims,
                expires: DateTime.UtcNow.AddHours(24),
                signingCredentials: credentials
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public async Task<bool> ChangePasswordAsync(int userId, ChangePasswordDto changePasswordDto)
        {
            try
            {
                var user = await _userRepository.GetByIdAsync(userId);
                if (user == null)
                {
                    return false;
                }

                // Verify current password
                if (!BCrypt.Net.BCrypt.Verify(changePasswordDto.CurrentPassword, user.PasswordHash))
                {
                    return false;
                }

                // Update password
                user.PasswordHash = BCrypt.Net.BCrypt.HashPassword(changePasswordDto.NewPassword);
                await _userRepository.UpdateAsync(user);

                _logger.LogInformation("Password changed successfully for user: {UserId}", userId);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error changing password for user: {UserId}", userId);
                return false;
            }
        }

        private static UserDto MapToUserDto(User user)
        {
            return new UserDto
            {
                Id = user.Id,
                Username = user.Username,
                Email = user.Email,
                FirstName = user.FirstName,
                LastName = user.LastName,
                IsActive = user.IsActive,
                CreatedAt = user.CreatedAt,
                UpdatedAt = user.UpdatedAt,
                LastLogin = user.LastLogin,
                RoleName = user.Role.RoleName
            };
        }

        public async Task<bool> LogoutAsync(string userId)
        {
            try
            {
                // For now, just log the logout
                _logger.LogInformation("User {UserId} logged out", userId);
                await Task.CompletedTask;
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error logging out user: {UserId}", userId);
                return false;
            }
        }
    }
}
