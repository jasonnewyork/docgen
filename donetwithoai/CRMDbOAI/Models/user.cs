using System;
using System.Collections.Generic;


namespace CRMDbOAI.Models;

public partial class user
{
    public int user_id { get; set; }
    public string username { get; set; } = null!;
    public string email { get; set; } = null!;
    public string first_name { get; set; } = null!;
    public string last_name { get; set; } = null!;
    public string password_hash { get; set; } = null!;
    public int role_id { get; set; }
    public bool? is_active { get; set; }
    public DateTime? created_date { get; set; }
    public DateTime? last_login_date { get; set; }
    public virtual ICollection<email_log> email_logs { get; set; } = new List<email_log>();
    public virtual role role { get; set; } = null!;
}
