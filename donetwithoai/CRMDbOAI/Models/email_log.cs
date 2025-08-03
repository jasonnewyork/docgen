using System;
using System.Collections.Generic;


namespace CRMDbOAI.Models;

public partial class email_log
{
    public int log_id { get; set; }
    public int? customer_id { get; set; }
    public int user_id { get; set; }
    public string email_type { get; set; } = null!;
    public string subject { get; set; } = null!;
    public string content { get; set; } = null!;
    public string recipient_email { get; set; } = null!;
    public DateTime? sent_date { get; set; }
    public string? status { get; set; }
    public string? error_message { get; set; }
    public virtual customer? customer { get; set; }
    public virtual user user { get; set; } = null!;
}
