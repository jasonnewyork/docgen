using System;
using System.Collections.Generic;


namespace CRMDbOAI.Models;

public partial class customer
{
    public int customer_id { get; set; }
    public string company_name { get; set; } = null!;
    public string? contact_first_name { get; set; }
    public string? contact_last_name { get; set; }
    public string? contact_email { get; set; }
    public string? contact_phone { get; set; }
    public string? address { get; set; }
    public string? city { get; set; }
    public string? state { get; set; }
    public string? country { get; set; }
    public string? postal_code { get; set; }
    public string? industry { get; set; }
    public DateTime? created_date { get; set; }
    public DateTime? last_modified_date { get; set; }
    public bool? is_active { get; set; }
    public virtual ICollection<email_log> email_logs { get; set; } = new List<email_log>();
}
