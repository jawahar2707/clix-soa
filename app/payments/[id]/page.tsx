'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { paymentAPI } from '@/lib/api';
import { ArrowLeft, Edit } from 'lucide-react';
import Link from 'next/link';
import { format } from 'date-fns';

export default function PaymentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = parseInt(params.id as string);
  const [payment, setPayment] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPayment();
  }, [id]);

  const loadPayment = async () => {
    try {
      setLoading(true);
      const response = await paymentAPI.getById(id);
      setPayment(response.data);
    } catch (error) {
      console.error('Error loading payment:', error);
      alert('Failed to load payment');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading...</div>;
  }

  if (!payment) {
    return <div className="p-8 text-center text-gray-500">Payment not found</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            href="/payments"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Payment #{payment.id}</h1>
            <p className="text-gray-600 mt-1">
              {format(new Date(payment.payment_date), 'MMMM dd, yyyy')}
            </p>
          </div>
        </div>
        <Link
          href={`/payments/${id}/edit`}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Edit className="h-4 w-4" />
          Edit
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Payment Details</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-sm text-gray-600">Customer</p>
            <p className="text-base font-medium text-gray-900 mt-1">
              {payment.customer?.name || `Customer ${payment.customer_id}`}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Amount</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">₹{payment.amount.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Payment Date</p>
            <p className="text-base text-gray-900 mt-1">
              {format(new Date(payment.payment_date), 'MMMM dd, yyyy')}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Due Date</p>
            <p className="text-base text-gray-900 mt-1">
              {format(new Date(payment.due_date), 'MMMM dd, yyyy')}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Status</p>
            <span
              className={`inline-block px-2 py-1 text-xs font-medium rounded-full mt-1 ${
                payment.status === 'paid'
                  ? 'bg-green-100 text-green-800'
                  : payment.status === 'overdue'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}
            >
              {payment.status}
            </span>
          </div>
          {payment.payment_method && (
            <div>
              <p className="text-sm text-gray-600">Payment Method</p>
              <p className="text-base text-gray-900 mt-1">{payment.payment_method}</p>
            </div>
          )}
          {payment.reference_number && (
            <div>
              <p className="text-sm text-gray-600">Reference Number</p>
              <p className="text-base text-gray-900 mt-1">{payment.reference_number}</p>
            </div>
          )}
          {payment.notes && (
            <div className="md:col-span-2">
              <p className="text-sm text-gray-600">Notes</p>
              <p className="text-base text-gray-900 mt-1">{payment.notes}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

