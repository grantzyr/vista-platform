'use client'

import { useEffect, useState } from 'react'
import { getProviders } from '@/apis/turnbench'
import { Main } from '@/components/layout/main'
import { columns } from './components/columns'
import { DataTable } from './components/data-table'
import { TasksDialogs } from './components/tasks-dialogs'
import { TasksPrimaryButtons } from './components/tasks-primary-buttons'
import TasksProvider from './context/tasks-context'

export default function Providers() {
  const [providersData, setProvidersData] = useState<
    { id: string; display_name: string; created_at: string, [key: string]: any }[]
  >([])
  const [providerParams, setProviderParams] = useState<{ page: number; page_size: number }>({
    page: 1,
    page_size : 10,
  });

  useEffect(() => {
    getProviders(providerParams).then((res: any) => {
      setProvidersData(res.data.data)
    })
  }, [])

  return (
    <TasksProvider>
      <Main>
        <div className='mb-2 flex flex-wrap items-center justify-between space-y-2 gap-x-4'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight'>Providers</h2>
            <p className='text-muted-foreground'>
              Here&apos;s a list of your Providers!
            </p>
          </div>
          <TasksPrimaryButtons />
        </div>
        <div className='-mx-4 flex-1 overflow-auto px-4 py-1 lg:flex-row lg:space-y-0 lg:space-x-12'>
          <DataTable data={providersData} columns={columns} />
        </div>
      </Main>

      <TasksDialogs />
    </TasksProvider>
  )
}
