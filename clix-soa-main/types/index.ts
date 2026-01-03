/**
 * TypeScript type definitions
 */

export interface Customer {
  id: number;
  name: string;
  contact?: string;
  email?: string;
  address?: string;
  status: string;
  credit_limit: number;
  credit_period_days: number;
  created_at: string;
  updated_at?: string;
}

export interface Inventory {
  id: number;
  product_code: string;
  product_name: string;
  category?: string;
  size?: string;
  available_quantity: number;
  reserved_quantity: number;
  unit: string;
  created_at: string;
  updated_at?: string;
}

export interface Order {
  id: number;
  customer_id: number;
  customer?: Customer;
  order_date: string;
  total_quantity: number;
  status: string;
  notes?: string;
  order_items?: OrderItem[];
  created_at: string;
  updated_at?: string;
}

export interface OrderItem {
  id: number;
  order_id: number;
  inventory_id: number;
  inventory?: Inventory;
  requested_quantity: number;
  allocated_quantity: number;
  created_at: string;
}

export interface Payment {
  id: number;
  customer_id: number;
  customer?: Customer;
  payment_date: string;
  amount: number;
  due_date: string;
  status: string;
  payment_method?: string;
  reference_number?: string;
  notes?: string;
  created_at: string;
}

export interface Allocation {
  id: number;
  order_id: number;
  inventory_id: number;
  inventory?: Inventory;
  allocated_quantity: number;
  allocation_date: string;
  algorithm_version: string;
  notes?: string;
}

export interface CustomerMetric {
  id: number;
  customer_id: number;
  customer?: Customer;
  total_orders: number;
  total_order_value: number;
  payment_frequency_score: number;
  credit_period_score: number;
  performance_score: number;
  overall_score: number;
  on_time_payment_percentage: number;
  average_days_to_payment: number;
  overdue_count: number;
  total_payments: number;
  last_calculated: string;
}

