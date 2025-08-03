using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using Serilog;
using MyCRM.Data;
using MyCRM.Repositories;
using MyCRM.Services;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .WriteTo.Console()
    .WriteTo.File("logs/mycrm-.log", rollingInterval: RollingInterval.Day)
    .CreateLogger();

builder.Host.UseSerilog();

// Add services to the container.
builder.Services.AddControllersWithViews();

// Configure Entity Framework
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
var sqlPassword = Environment.GetEnvironmentVariable("SQL_PASSWORD");
if (!string.IsNullOrEmpty(sqlPassword))
{
    connectionString = connectionString?.Replace("Password=;", $"Password={sqlPassword};");
}

builder.Services.AddDbContext<CrmDbContext>(options =>
    options.UseSqlServer(connectionString));

// Configure JWT Authentication - temporarily disabled for minimal setup
/*
var jwtSecretKey = Environment.GetEnvironmentVariable("JWT_SECRET_KEY") 
    ?? builder.Configuration["JWT:SecretKey"]
    ?? throw new InvalidOperationException("JWT secret key must be configured");

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["JWT:Issuer"],
            ValidAudience = builder.Configuration["JWT:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSecretKey))
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => 
        policy.RequireRole("Administrator"));
    options.AddPolicy("PowerUserOrAdmin", policy => 
        policy.RequireRole("Administrator", "PowerUser"));
    options.AddPolicy("AllUsers", policy => 
        policy.RequireRole("Administrator", "PowerUser", "CustomerManager"));
});
*/

// Register repositories  
// builder.Services.AddScoped<IUserRepository, UserRepository>();  // Temporarily disabled for property alignment
// builder.Services.AddScoped<IUserRoleRepository, UserRoleRepository>();  // Temporarily disabled
builder.Services.AddScoped<IEmailLogRepository, MyCRM.Repositories.EmailLogRepository>();

// CustomerRepository registration re-enabled for core functionality
builder.Services.AddScoped<ICustomerRepository, MyCRM.Repositories.CustomerRepository>();

// Register services - re-enabled core services
// builder.Services.AddScoped<IAuthService, AuthService>();  // Temporarily disabled until User services are fixed
builder.Services.AddScoped<EmailService>();

// CustomerService registration temporarily disabled for basic testing  
// builder.Services.AddScoped<CustomerService>();
// builder.Services.AddScoped<MyCRM.Services.UserService>();

// Configure CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("DefaultPolicy", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Configure Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo 
    { 
        Title = "MyCRM API", 
        Version = "v1",
        Description = "Customer Relationship Management System with AI Email Generation"
    });
    
    // JWT Security requirements temporarily disabled for minimal setup
    /*
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using the Bearer scheme",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });
    
    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            new string[] {}
        }
    });
    */
});

// Configure session
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(
        builder.Configuration.GetValue<int>("Security:SessionTimeoutMinutes", 30));
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "MyCRM API V1");
        c.RoutePrefix = "api-docs";
    });
    
    // Disable HTTPS redirection in development
    // app.UseHttpsRedirection();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
    app.UseHttpsRedirection();
}
app.UseStaticFiles();

app.UseRouting();

app.UseCors("DefaultPolicy");
// app.UseAuthentication();  // Temporarily disabled
// app.UseAuthorization();   // Temporarily disabled
app.UseSession();

// Custom middleware for request logging
app.Use(async (context, next) =>
{
    var stopwatch = System.Diagnostics.Stopwatch.StartNew();
    await next();
    stopwatch.Stop();
    
    Log.Information("Request {Method} {Url} responded {StatusCode} in {Elapsed:0.0000} ms",
        context.Request.Method,
        context.Request.Path,
        context.Response.StatusCode,
        stopwatch.ElapsedMilliseconds);
});

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// API routes
app.MapControllerRoute(
    name: "api",
    pattern: "api/{controller}/{action=Index}/{id?}");

// Ensure database is created and seeded
try
{
    using var scope = app.Services.CreateScope();
    var context = scope.ServiceProvider.GetRequiredService<CrmDbContext>();
    
    // Check if database exists and is accessible
    if (context.Database.CanConnect())
    {
        Log.Information("Database connection successful");
        
        // Apply any pending migrations
        var pendingMigrations = context.Database.GetPendingMigrations();
        if (pendingMigrations.Any())
        {
            Log.Information("Applying {Count} pending migrations", pendingMigrations.Count());
            context.Database.Migrate();
            Log.Information("Database migrations applied successfully");
        }
    }
    else
    {
        Log.Warning("Cannot connect to database. Application will start but database features may not work.");
    }
}
catch (Exception ex)
{
    Log.Error(ex, "An error occurred while initializing the database");
}

Log.Information("MyCRM application starting...");

app.Run();
