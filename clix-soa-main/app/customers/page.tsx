'use client';

import { useEffect, useState } from 'react';
import { customerAPI } from '@/lib/api';
import { exportCustomers } from '@/lib/csv-utils';
import { Plus, Search, Edit, Trash2 } from 'lucide-react';
import Link from 'next/link';
import ImportExport from '@/components/ImportExport';

interface Customer {
  id: number;
  name: string;
  contact?: string;
  email?: string;
  address?: string;
  status: string;
  credit_limit: number;
  credit_period_days: number;
  created_at: string;
}

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      const response = await customerAPI.getAll(0, 1000);
      setCustomers(response.data);
    } catch (error) {
      console.error('Error loading customers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async (data: any[]) => {
    let successCount = 0;
    let errorCount = 0;

    for (const row of data) {
      try {
        await customerAPI.create({
          name: row.Name || row.name || '',
          contact: row.Contact || row.contact || row.Mobile_1 || row.Mobile_2 || '',
          email: row.Email || row.email || row.Email_1 || row.Email_2 || '',
          address: row.Address || row.address || '',
          credit_limit: parseFloat(row['Credit Limit'] || row.credit_limit || '0') || 0,
          credit_period_days: parseInt(row['Credit Period (Days)'] || row.credit_period_days || '30') || 30,
        });
        successCount++;
      } catch (error) {
        errorCount++;
        console.error('Error importing customer:', error);
      }
    }

    if (successCount > 0) {
      await loadCustomers();
    }

    if (errorCount > 0) {
      throw new Error(`${successCount} imported, ${errorCount} failed`);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this customer?')) return;

    try {
      await customerAPI.delete(id);
      loadCustomers();
    } catch (error) {
      console.error('Error deleting customer:', error);
      alert('Failed to delete customer');
    }
  };

  const filteredCustomers = customers.filter((customer) =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.contact?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Customers</h1>
          <p className="text-gray-600 mt-1">Manage your customer database</p>
        </div>
        <div className="flex items-center gap-3">
          <ImportExport
            onImport={handleImport}
            exportData={customers}
            exportFilename="customers"
            importFields={['Name', 'Contact', 'Email', 'Address', 'Credit Limit', 'Credit Period (Days)']}
            title="Import Customers"
          />
          <Link
            href="/customers/new"
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="h-4 w-4" />
            Add Customer
          </Link>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search customers by name, contact, or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Customers Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading customers...</div>
        ) : filteredCustomers.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No customers found</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Credit Limit
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredCustomers.map((customer) => (
                  <tr key={customer.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {customer.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{customer.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {customer.contact || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {customer.email || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ₹{customer.credit_limit.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 text-xs font-medium rounded-full ${
                          customer.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {customer.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end gap-2">
                        <Link
                          href={`/customers/${customer.id}`}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          <Edit className="h-4 w-4" />
                        </Link>
                        <button
                          onClick={() => handleDelete(customer.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <p className="text-sm text-gray-600">
            Showing {filteredCustomers.length} of {customers.length} customers
          </p>
        </div>
      </div>

    </div>
  );
}

