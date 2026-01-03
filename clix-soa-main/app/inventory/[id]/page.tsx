'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { inventoryAPI } from '@/lib/api';
import { ArrowLeft, Save } from 'lucide-react';
import Link from 'next/link';

export default function InventoryDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = parseInt(params.id as string);
  const isNew = params.id === 'new';

  const [formData, setFormData] = useState({
    product_code: '',
    product_name: '',
    category: '',
    size: '',
    available_quantity: 0,
    reserved_quantity: 0,
    unit: 'PCS',
  });
  const [loading, setLoading] = useState(!isNew);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!isNew) {
      loadInventory();
    }
  }, [id]);

  const loadInventory = async () => {
    try {
      setLoading(true);
      const response = await inventoryAPI.getById(id);
      setFormData({
        product_code: response.data.product_code,
        product_name: response.data.product_name,
        category: response.data.category || '',
        size: response.data.size || '',
        available_quantity: response.data.available_quantity || 0,
        reserved_quantity: response.data.reserved_quantity || 0,
        unit: response.data.unit || 'PCS',
      });
    } catch (error) {
      console.error('Error loading inventory:', error);
      alert('Failed to load inventory item');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      if (isNew) {
        await inventoryAPI.create(formData);
      } else {
        await inventoryAPI.update(id, formData);
      }
      router.push('/inventory');
    } catch (error) {
      console.error('Error saving inventory:', error);
      alert('Failed to save inventory item');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link
          href="/inventory"
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <h1 className="text-3xl font-bold text-gray-900">
          {isNew ? 'Add Inventory Item' : 'Edit Inventory Item'}
        </h1>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Code *
            </label>
            <input
              type="text"
              required
              value={formData.product_code}
              onChange={(e) => setFormData({ ...formData, product_code: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Name *
            </label>
            <input
              type="text"
              required
              value={formData.product_name}
              onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <input
              type="text"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Size
            </label>
            <input
              type="text"
              placeholder="45-110 or XS, S, M, L, XL, XXL"
              value={formData.size}
              onChange={(e) => setFormData({ ...formData, size: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Available Quantity *
            </label>
            <input
              type="number"
              step="0.01"
              required
              value={formData.available_quantity}
              onChange={(e) => setFormData({ ...formData, available_quantity: parseFloat(e.target.value) || 0 })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Unit
            </label>
            <select
              value={formData.unit}
              onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="PCS">PCS</option>
              <option value="KGS">KGS</option>
              <option value="MTR">MTR</option>
              <option value="SET">SET</option>
            </select>
          </div>
        </div>

        {!isNew && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Reserved Quantity
            </label>
            <input
              type="number"
              step="0.01"
              value={formData.reserved_quantity}
              onChange={(e) => setFormData({ ...formData, reserved_quantity: parseFloat(e.target.value) || 0 })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        )}

        <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
          <Link
            href="/inventory"
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Cancel
          </Link>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Save className="h-4 w-4" />
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </form>
    </div>
  );
}

