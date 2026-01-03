'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { orderAPI } from '@/lib/api';
import { ArrowLeft, Edit } from 'lucide-react';
import Link from 'next/link';
import { format } from 'date-fns';

export default function OrderDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = parseInt(params.id as string);
  const [order, setOrder] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrder();
  }, [id]);

  const loadOrder = async () => {
    try {
      setLoading(true);
      const response = await orderAPI.getById(id);
      setOrder(response.data);
    } catch (error) {
      console.error('Error loading order:', error);
      alert('Failed to load order');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading...</div>;
  }

  if (!order) {
    return <div className="p-8 text-center text-gray-500">Order not found</div>;
  }

  const statusColors: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    allocated: 'bg-blue-100 text-blue-800',
    partially_allocated: 'bg-orange-100 text-orange-800',
    fulfilled: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            href="/orders"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Order #{order.id}</h1>
            <p className="text-gray-600 mt-1">
              {format(new Date(order.order_date), 'MMMM dd, yyyy')}
            </p>
          </div>
        </div>
        <Link
          href={`/orders/${id}/edit`}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Edit className="h-4 w-4" />
          Edit
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Order Information</h2>
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-600">Customer</p>
              <p className="text-base font-medium text-gray-900">
                {order.customer?.name || `Customer ${order.customer_id}`}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <span
                className={`inline-block px-2 py-1 text-xs font-medium rounded-full mt-1 ${
                  statusColors[order.status] || 'bg-gray-100 text-gray-800'
                }`}
              >
                {order.status.replace('_', ' ')}
              </span>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Quantity</p>
              <p className="text-base font-medium text-gray-900">{order.total_quantity.toLocaleString()}</p>
            </div>
            {order.notes && (
              <div>
                <p className="text-sm text-gray-600">Notes</p>
                <p className="text-base text-gray-900">{order.notes}</p>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Order Items</h2>
          {order.order_items && order.order_items.length > 0 ? (
            <div className="space-y-3">
              {order.order_items.map((item: any) => (
                <div key={item.id} className="border-b border-gray-200 pb-3 last:border-0">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">
                        {item.inventory?.product_code || `Item ${item.inventory_id}`}
                      </p>
                      <p className="text-sm text-gray-600">
                        {item.inventory?.product_name || ''}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Requested</p>
                      <p className="font-medium text-gray-900">{item.requested_quantity}</p>
                      <p className="text-sm text-green-600 mt-1">Allocated: {item.allocated_quantity}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No items in this order</p>
          )}
        </div>
      </div>
    </div>
  );
}

