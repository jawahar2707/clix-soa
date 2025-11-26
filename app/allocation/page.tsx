'use client';

import { useEffect, useState } from 'react';
import { allocationAPI, orderAPI } from '@/lib/api';
import { exportAllocations } from '@/lib/csv-utils';
import { Zap, RefreshCw, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { format } from 'date-fns';
import ImportExport from '@/components/ImportExport';

interface AllocationResult {
  order_id: number;
  customer_id: number;
  customer_name: string;
  total_requested: number;
  total_allocated: number;
  allocation_percentage: number;
  items: Array<{
    inventory_id: number;
    product_code: string;
    product_name: string;
    requested: number;
    allocated: number;
  }>;
  success: boolean;
  message: string;
}

export default function AllocationPage() {
  const [results, setResults] = useState<AllocationResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [allocating, setAllocating] = useState(false);
  const [selectedOrders, setSelectedOrders] = useState<number[]>([]);
  const [recalculateMetrics, setRecalculateMetrics] = useState(true);
  const [allocationHistory, setAllocationHistory] = useState<any[]>([]);

  useEffect(() => {
    loadAllocationHistory();
  }, []);

  const loadAllocationHistory = async () => {
    try {
      const response = await allocationAPI.getHistory({ limit: 100 });
      setAllocationHistory(response.data);
    } catch (error) {
      console.error('Error loading allocation history:', error);
    }
  };

  const handleAllocate = async () => {
    try {
      setAllocating(true);
      const response = await allocationAPI.allocate({
        order_ids: selectedOrders.length > 0 ? selectedOrders : undefined,
        recalculate_metrics: recalculateMetrics,
      });
      setResults(response.data);
      loadAllocationHistory();
    } catch (error) {
      console.error('Error allocating orders:', error);
      alert('Failed to allocate orders. Please check the server connection.');
    } finally {
      setAllocating(false);
    }
  };

  const handleExport = () => {
    exportAllocations(allocationHistory);
  };

  const totalRequested = results.reduce((sum, r) => sum + r.total_requested, 0);
  const totalAllocated = results.reduce((sum, r) => sum + r.total_allocated, 0);
  const overallPercentage = totalRequested > 0 ? (totalAllocated / totalRequested) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Order Allocation</h1>
          <p className="text-gray-600 mt-1">Allocate orders based on customer performance</p>
        </div>
        <div className="flex items-center gap-3">
          <ImportExport
            exportData={allocationHistory}
            exportFilename="allocation_history"
            title="Export Allocation History"
          />
          <button
            onClick={handleAllocate}
            disabled={allocating}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {allocating ? (
              <>
                <RefreshCw className="h-4 w-4 animate-spin" />
                Allocating...
              </>
            ) : (
              <>
                <Zap className="h-4 w-4" />
                Allocate Orders
              </>
            )}
          </button>
        </div>
      </div>

      {/* Allocation Settings */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Allocation Settings</h2>
        <div className="space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="recalculate"
              checked={recalculateMetrics}
              onChange={(e) => setRecalculateMetrics(e.target.checked)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="recalculate" className="ml-2 text-sm text-gray-700">
              Recalculate customer metrics before allocation
            </label>
          </div>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Allocation Algorithm:</strong> Orders are allocated based on customer performance (30%),
              payment frequency (25%), credit period adherence (25%), and stock availability (20%).
            </p>
          </div>
        </div>
      </div>

      {/* Allocation Results */}
      {results.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Allocation Results</h2>
            <div className="text-right">
              <p className="text-sm text-gray-600">Overall Allocation</p>
              <p className="text-2xl font-bold text-gray-900">
                {overallPercentage.toFixed(1)}%
              </p>
              <p className="text-sm text-gray-500">
                {totalAllocated.toLocaleString()} / {totalRequested.toLocaleString()}
              </p>
            </div>
          </div>

          <div className="space-y-4">
            {results.map((result) => (
              <div
                key={result.order_id}
                className={`border rounded-lg p-4 ${
                  result.success
                    ? 'border-green-200 bg-green-50'
                    : 'border-red-200 bg-red-50'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      {result.success ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-600" />
                      )}
                      <div>
                        <p className="font-medium text-gray-900">
                          Order #{result.order_id} - {result.customer_name}
                        </p>
                        <p className="text-sm text-gray-600">{result.message}</p>
                      </div>
                    </div>
                    <div className="ml-8 space-y-2">
                      <div className="flex items-center gap-4 text-sm">
                        <span className="text-gray-600">Requested:</span>
                        <span className="font-medium">{result.total_requested.toLocaleString()}</span>
                        <span className="text-gray-600">Allocated:</span>
                        <span className="font-medium text-green-600">
                          {result.total_allocated.toLocaleString()}
                        </span>
                        <span className="text-gray-600">Percentage:</span>
                        <span className="font-medium">{result.allocation_percentage.toFixed(1)}%</span>
                      </div>
                      {result.items.length > 0 && (
                        <div className="mt-3">
                          <p className="text-xs font-medium text-gray-700 mb-1">Items:</p>
                          <div className="space-y-1">
                            {result.items.map((item, idx) => (
                              <div key={idx} className="text-xs text-gray-600 pl-4">
                                {item.product_code} ({item.product_name}): {item.allocated} / {item.requested}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Allocation History */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Allocation History</h2>
        </div>
        {allocationHistory.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No allocation history</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Order ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Product
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Allocated Quantity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Algorithm Version
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {allocationHistory.map((allocation) => (
                  <tr key={allocation.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {format(new Date(allocation.allocation_date), 'MMM dd, yyyy HH:mm')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      #{allocation.order_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {allocation.inventory?.product_code || `Item ${allocation.inventory_id}`}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {allocation.allocated_quantity.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {allocation.algorithm_version}
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

