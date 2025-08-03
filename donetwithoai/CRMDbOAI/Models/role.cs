﻿using System;
using System.Collections.Generic;


namespace CRMDbOAI.Models;

public partial class role
{
    public int role_id { get; set; }
    public string role_name { get; set; } = null!;
    public string? description { get; set; }
    public DateTime? created_date { get; set; }
    public virtual ICollection<user> users { get; set; } = new List<user>();
}
