/**
 * CSV Import/Export Utilities
 */
import Papa from 'papaparse';

export interface CSVImportResult {
  success: boolean;
  data: any[];
  errors: string[];
  totalRows: number;
  importedRows: number;
}

/**
 * Parse CSV file
 */
export function parseCSV(file: File): Promise<CSVImportResult> {
  return new Promise((resolve) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        const errors: string[] = [];
        const data: any[] = [];

        results.data.forEach((row: any, index: number) => {
          try {
            // Clean up row data
            const cleanRow: any = {};
            Object.keys(row).forEach((key) => {
              const cleanKey = key.trim();
              const value = row[key];
              if (value !== undefined && value !== null && value !== '') {
                cleanRow[cleanKey] = String(value).trim();
              }
            });

            if (Object.keys(cleanRow).length > 0) {
              data.push(cleanRow);
            }
          } catch (error) {
            errors.push(`Row ${index + 1}: ${error}`);
          }
        });

        resolve({
          success: errors.length === 0,
          data,
          errors,
          totalRows: results.data.length,
          importedRows: data.length,
        });
      },
      error: (error) => {
        resolve({
          success: false,
          data: [],
          errors: [error.message],
          totalRows: 0,
          importedRows: 0,
        });
      },
    });
  });
}

/**
 * Export data to CSV
 */
export function exportToCSV(data: any[], filename: string) {
  const csv = Papa.unparse(data);
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  URL.revokeObjectURL(url);
}

/**
 * Export customers to CSV
 */
export function exportCustomers(customers: any[]) {
  const csvData = customers.map((customer) => ({
    ID: customer.id,
    Name: customer.name,
    Contact: customer.contact || '',
    Email: customer.email || '',
    Address: customer.address || '',
    Status: customer.status,
    'Credit Limit': customer.credit_limit || 0,
    'Credit Period (Days)': customer.credit_period_days || 30,
    'Created At': customer.created_at,
  }));
  
  exportToCSV(csvData, `customers_${new Date().toISOString().split('T')[0]}.csv`);
}

/**
 * Export inventory to CSV
 */
export function exportInventory(inventory: any[]) {
  const csvData = inventory.map((item) => ({
    ID: item.id,
    'Product Code': item.product_code,
    'Product Name': item.product_name,
    Category: item.category || '',
    Size: item.size || '',
    'Available Quantity': item.available_quantity,
    'Reserved Quantity': item.reserved_quantity,
    Unit: item.unit,
    'Created At': item.created_at,
  }));
  
  exportToCSV(csvData, `inventory_${new Date().toISOString().split('T')[0]}.csv`);
}

/**
 * Export orders to CSV
 */
export function exportOrders(orders: any[]) {
  const csvData = orders.map((order) => ({
    'Order ID': order.id,
    'Customer ID': order.customer_id,
    'Customer Name': order.customer?.name || '',
    'Order Date': order.order_date,
    'Total Quantity': order.total_quantity,
    Status: order.status,
    Notes: order.notes || '',
    'Created At': order.created_at,
  }));
  
  exportToCSV(csvData, `orders_${new Date().toISOString().split('T')[0]}.csv`);
}

/**
 * Export payments to CSV
 */
export function exportPayments(payments: any[]) {
  const csvData = payments.map((payment) => ({
    'Payment ID': payment.id,
    'Customer ID': payment.customer_id,
    'Customer Name': payment.customer?.name || '',
    'Payment Date': payment.payment_date,
    Amount: payment.amount,
    'Due Date': payment.due_date,
    Status: payment.status,
    'Payment Method': payment.payment_method || '',
    'Reference Number': payment.reference_number || '',
    Notes: payment.notes || '',
  }));
  
  exportToCSV(csvData, `payments_${new Date().toISOString().split('T')[0]}.csv`);
}

/**
 * Export allocations to CSV
 */
export function exportAllocations(allocations: any[]) {
  const csvData = allocations.map((allocation) => ({
    'Allocation ID': allocation.id,
    'Order ID': allocation.order_id,
    'Inventory ID': allocation.inventory_id,
    'Product Code': allocation.inventory?.product_code || '',
    'Product Name': allocation.inventory?.product_name || '',
    'Allocated Quantity': allocation.allocated_quantity,
    'Allocation Date': allocation.allocation_date,
    'Algorithm Version': allocation.algorithm_version,
  }));
  
  exportToCSV(csvData, `allocations_${new Date().toISOString().split('T')[0]}.csv`);
}

/**
 * Export customer metrics to CSV
 */
export function exportCustomerMetrics(metrics: any[]) {
  const csvData = metrics.map((metric) => ({
    'Customer ID': metric.customer_id,
    'Customer Name': metric.customer?.name || '',
    'Overall Score': metric.overall_score,
    'Performance Score': metric.performance_score,
    'Payment Frequency Score': metric.payment_frequency_score,
    'Credit Period Score': metric.credit_period_score,
    'Total Orders': metric.total_orders,
    'Total Order Value': metric.total_order_value,
    'On-Time Payment %': metric.on_time_payment_percentage,
    'Average Days to Payment': metric.average_days_to_payment,
    'Overdue Count': metric.overdue_count,
    'Total Payments': metric.total_payments,
    'Last Calculated': metric.last_calculated,
  }));
  
  exportToCSV(csvData, `customer_metrics_${new Date().toISOString().split('T')[0]}.csv`);
}

