/**
 * API Client for Order Allocation System
 */
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Customer APIs
export const customerAPI = {
  getAll: (skip = 0, limit = 100) => api.get(`/customers/?skip=${skip}&limit=${limit}`),
  getById: (id: number) => api.get(`/customers/${id}`),
  create: (data: any) => api.post('/customers/', data),
  update: (id: number, data: any) => api.put(`/customers/${id}`, data),
  delete: (id: number) => api.delete(`/customers/${id}`),
};

// Inventory APIs
export const inventoryAPI = {
  getAll: (skip = 0, limit = 100) => api.get(`/inventory/?skip=${skip}&limit=${limit}`),
  getById: (id: number) => api.get(`/inventory/${id}`),
  getByCode: (code: string) => api.get(`/inventory/code/${code}`),
  create: (data: any) => api.post('/inventory/', data),
  update: (id: number, data: any) => api.put(`/inventory/${id}`, data),
  delete: (id: number) => api.delete(`/inventory/${id}`),
};

// Order APIs
export const orderAPI = {
  getAll: (params?: { skip?: number; limit?: number; status?: string; customer_id?: number }) => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.status) queryParams.append('status', params.status);
    if (params?.customer_id) queryParams.append('customer_id', params.customer_id.toString());
    return api.get(`/orders/?${queryParams.toString()}`);
  },
  getById: (id: number) => api.get(`/orders/${id}`),
  create: (data: any) => api.post('/orders/', data),
  update: (id: number, data: any) => api.put(`/orders/${id}`, data),
  delete: (id: number) => api.delete(`/orders/${id}`),
};

// Payment APIs
export const paymentAPI = {
  getAll: (params?: { skip?: number; limit?: number; customer_id?: number; status?: string }) => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.customer_id) queryParams.append('customer_id', params.customer_id.toString());
    if (params?.status) queryParams.append('status', params.status);
    return api.get(`/payments/?${queryParams.toString()}`);
  },
  getById: (id: number) => api.get(`/payments/${id}`),
  create: (data: any) => api.post('/payments/', data),
  update: (id: number, data: any) => api.put(`/payments/${id}`, data),
  delete: (id: number) => api.delete(`/payments/${id}`),
};

// Allocation APIs
export const allocationAPI = {
  allocate: (data: { order_ids?: number[]; recalculate_metrics?: boolean }) =>
    api.post('/allocation/allocate', data),
  getHistory: (params?: { skip?: number; limit?: number; order_id?: number; inventory_id?: number }) => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.order_id) queryParams.append('order_id', params.order_id.toString());
    if (params?.inventory_id) queryParams.append('inventory_id', params.inventory_id.toString());
    return api.get(`/allocation/history?${queryParams.toString()}`);
  },
  getByOrder: (orderId: number) => api.get(`/allocation/order/${orderId}`),
};

// Metrics APIs
export const metricsAPI = {
  getCustomerMetrics: (customerId: number) => api.get(`/metrics/customer/${customerId}`),
  recalculateCustomer: (customerId: number) => api.post(`/metrics/customer/${customerId}/recalculate`),
  recalculateAll: () => api.post('/metrics/recalculate-all'),
};

// Health check
export const healthCheck = () => api.get('/health');

export default api;

