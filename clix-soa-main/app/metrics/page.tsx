'use client';

import { useEffect, useState } from 'react';
import { metricsAPI, customerAPI } from '@/lib/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { RefreshCw, TrendingUp, TrendingDown } from 'lucide-react';
import ImportExport from '@/components/ImportExport';

interface CustomerMetric {
  id: number;
  customer_id: number;
  customer?: { name: string };
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
}

export default function MetricsPage() {
  const [metrics, setMetrics] = useState<CustomerMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [recalculating, setRecalculating] = useState(false);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      setLoading(true);
      // Get all customers and their metrics
      const customersRes = await customerAPI.getAll(0, 1000);
      const customers = customersRes.data;

      // Fetch metrics for each customer
      const metricsPromises = customers.map(async (customer: any) => {
        try {
          const metricsRes = await metricsAPI.getCustomerMetrics(customer.id);
          return { ...metricsRes.data, customer };
        } catch {
          return null;
        }
      });

      const allMetrics = (await Promise.all(metricsPromises)).filter((m) => m !== null);
      setMetrics(allMetrics);
    } catch (error) {
      console.error('Error loading metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRecalculateAll = async () => {
    try {
      setRecalculating(true);
      await metricsAPI.recalculateAll();
      alert('Metrics recalculated successfully!');
      loadMetrics();
    } catch (error) {
      console.error('Error recalculating metrics:', error);
      alert('Failed to recalculate metrics');
    } finally {
      setRecalculating(false);
    }
  };

  // Prepare chart data
  const topCustomers = [...metrics]
    .sort((a, b) => b.overall_score - a.overall_score)
    .slice(0, 10)
    .map((m) => ({
      name: m.customer?.name || `Customer ${m.customer_id}`,
      score: m.overall_score,
      performance: m.performance_score,
      payment: m.payment_frequency_score,
      credit: m.credit_period_score,
    }));

  const avgMetrics = {
    performance: metrics.reduce((sum, m) => sum + m.performance_score, 0) / metrics.length || 0,
    payment: metrics.reduce((sum, m) => sum + m.payment_frequency_score, 0) / metrics.length || 0,
    credit: metrics.reduce((sum, m) => sum + m.credit_period_score, 0) / metrics.length || 0,
    overall: metrics.reduce((sum, m) => sum + m.overall_score, 0) / metrics.length || 0,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Customer Metrics</h1>
          <p className="text-gray-600 mt-1">Customer performance and allocation scores</p>
        </div>
        <div className="flex items-center gap-3">
          <ImportExport
            exportData={metrics.map(m => ({
              'Customer ID': m.customer_id,
              'Customer Name': m.customer?.name || '',
              'Overall Score': m.overall_score,
              'Performance Score': m.performance_score,
              'Payment Frequency Score': m.payment_frequency_score,
              'Credit Period Score': m.credit_period_score,
              'Total Orders': m.total_orders,
              'Total Order Value': m.total_order_value,
              'On-Time Payment %': m.on_time_payment_percentage,
              'Average Days to Payment': m.average_days_to_payment,
              'Overdue Count': m.overdue_count,
              'Total Payments': m.total_payments,
            }))}
            exportFilename="customer_metrics"
            title="Export Customer Metrics"
          />
          <button
            onClick={handleRecalculateAll}
            disabled={recalculating}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {recalculating ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Recalculating...
              </>
            ) : (
              <>
                <RefreshCw className="h-4 w-4" />
                Recalculate All
              </>
            )}
          </button>
        </div>
      </div>

      {/* Average Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">Avg Performance</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{avgMetrics.performance.toFixed(1)}</p>
          <p className="text-xs text-gray-500 mt-1">Out of 100</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">Avg Payment Score</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{avgMetrics.payment.toFixed(1)}</p>
          <p className="text-xs text-gray-500 mt-1">Out of 100</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">Avg Credit Score</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{avgMetrics.credit.toFixed(1)}</p>
          <p className="text-xs text-gray-500 mt-1">Out of 100</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">Avg Overall Score</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{avgMetrics.overall.toFixed(1)}</p>
          <p className="text-xs text-gray-500 mt-1">Out of 100</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Top 10 Customers by Overall Score</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topCustomers}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="score" fill="#3b82f6" name="Overall Score" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Score Breakdown (Top 10)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topCustomers}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="performance" fill="#10b981" name="Performance" />
              <Bar dataKey="payment" fill="#f59e0b" name="Payment" />
              <Bar dataKey="credit" fill="#ef4444" name="Credit" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Metrics Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">All Customer Metrics</h2>
        </div>
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading metrics...</div>
        ) : metrics.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No metrics available</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Overall Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Performance
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Payment
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Credit
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Orders
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    On-Time %
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {metrics
                  .sort((a, b) => b.overall_score - a.overall_score)
                  .map((metric) => (
                    <tr key={metric.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {metric.customer?.name || `Customer ${metric.customer_id}`}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <span className="text-sm font-bold text-gray-900">
                            {metric.overall_score.toFixed(1)}
                          </span>
                          {metric.overall_score >= 70 ? (
                            <TrendingUp className="h-4 w-4 text-green-500 ml-2" />
                          ) : (
                            <TrendingDown className="h-4 w-4 text-red-500 ml-2" />
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {metric.performance_score.toFixed(1)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {metric.payment_frequency_score.toFixed(1)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {metric.credit_period_score.toFixed(1)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {metric.total_orders}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {metric.on_time_payment_percentage.toFixed(1)}%
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

