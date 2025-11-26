'use client';

import { useState, useRef } from 'react';
import { Upload, Download, FileSpreadsheet, X, CheckCircle, AlertCircle } from 'lucide-react';
import { parseCSV, exportToCSV, CSVImportResult } from '@/lib/csv-utils';
import Papa from 'papaparse';

interface ImportExportProps {
  onImport?: (data: any[]) => Promise<void>;
  onExport?: () => void;
  exportData?: any[];
  exportFilename?: string;
  importTemplate?: any[];
  importFields?: string[];
  title?: string;
}

export default function ImportExport({
  onImport,
  onExport,
  exportData,
  exportFilename = 'export',
  importTemplate,
  importFields,
  title = 'Import / Export',
}: ImportExportProps) {
  const [importing, setImporting] = useState(false);
  const [importResult, setImportResult] = useState<CSVImportResult | null>(null);
  const [showImportModal, setShowImportModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setImporting(true);
    setImportResult(null);

    try {
      const result = await parseCSV(file);
      setImportResult(result);

      if (result.success && result.data.length > 0 && onImport) {
        try {
          await onImport(result.data);
          setImportResult({
            ...result,
            success: true,
          });
        } catch (error: any) {
          setImportResult({
            ...result,
            success: false,
            errors: [...result.errors, error.message || 'Import failed'],
          });
        }
      }
    } catch (error: any) {
      setImportResult({
        success: false,
        data: [],
        errors: [error.message || 'Failed to parse CSV'],
        totalRows: 0,
        importedRows: 0,
      });
    } finally {
      setImporting(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleExport = () => {
    if (exportData && exportData.length > 0) {
      exportToCSV(exportData, `${exportFilename}_${new Date().toISOString().split('T')[0]}.csv`);
    } else if (onExport) {
      onExport();
    }
  };

  const handleDownloadTemplate = () => {
    if (importTemplate && importTemplate.length > 0) {
      exportToCSV(importTemplate, `import_template_${exportFilename}.csv`);
    } else if (importFields) {
      // Create template with headers only
      const template = [importFields.reduce((acc, field) => ({ ...acc, [field]: '' }), {})];
      exportToCSV(template, `import_template_${exportFilename}.csv`);
    }
  };

  return (
    <div className="flex items-center gap-2">
      {/* Export Button */}
      {(exportData || onExport) && (
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
        >
          <Download className="h-4 w-4" />
          Export CSV
        </button>
      )}

      {/* Import Button */}
      {onImport && (
        <>
          <button
            onClick={() => setShowImportModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
          >
            <Upload className="h-4 w-4" />
            Import CSV
          </button>

          {/* Import Template Download */}
          {(importTemplate || importFields) && (
            <button
              onClick={handleDownloadTemplate}
              className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium"
              title="Download import template"
            >
              <FileSpreadsheet className="h-4 w-4" />
              Template
            </button>
          )}
        </>
      )}

      {/* Import Modal */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-gray-900">{title}</h2>
                <button
                  onClick={() => {
                    setShowImportModal(false);
                    setImportResult(null);
                  }}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
            </div>

            <div className="p-6 space-y-4">
              {/* File Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select CSV File
                </label>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv"
                  onChange={handleFileSelect}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
              </div>

              {/* Import Result */}
              {importResult && (
                <div
                  className={`p-4 rounded-lg border ${
                    importResult.success
                      ? 'bg-green-50 border-green-200'
                      : 'bg-red-50 border-red-200'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    {importResult.success ? (
                      <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
                    ) : (
                      <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                    )}
                    <div className="flex-1">
                      <p
                        className={`font-medium ${
                          importResult.success ? 'text-green-800' : 'text-red-800'
                        }`}
                      >
                        {importResult.success ? 'Import Successful!' : 'Import Failed'}
                      </p>
                      <div className="mt-2 text-sm space-y-1">
                        <p className={importResult.success ? 'text-green-700' : 'text-red-700'}>
                          Total Rows: {importResult.totalRows}
                        </p>
                        <p className={importResult.success ? 'text-green-700' : 'text-red-700'}>
                          Imported: {importResult.importedRows}
                        </p>
                        {importResult.errors.length > 0 && (
                          <div className="mt-2">
                            <p className="font-medium text-red-800">Errors:</p>
                            <ul className="list-disc list-inside text-red-700 text-xs mt-1 space-y-1">
                              {importResult.errors.map((error, idx) => (
                                <li key={idx}>{error}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Loading State */}
              {importing && (
                <div className="text-center py-4">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <p className="mt-2 text-sm text-gray-600">Importing data...</p>
                </div>
              )}

              {/* Instructions */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm font-medium text-gray-700 mb-2">Import Instructions:</p>
                <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
                  <li>CSV file must have headers in the first row</li>
                  <li>Empty rows will be skipped</li>
                  <li>Download template for correct format</li>
                  {importFields && (
                    <li>Required fields: {importFields.join(', ')}</li>
                  )}
                </ul>
              </div>
            </div>

            <div className="p-6 border-t border-gray-200 flex justify-end gap-3">
              <button
                onClick={() => {
                  setShowImportModal(false);
                  setImportResult(null);
                }}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

