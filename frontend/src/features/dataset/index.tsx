'use client'

import { useEffect, useState } from 'react'
import { getSetUps } from '@/apis/turnbench'
import { Main } from '@/components/layout/main'
import { columns } from './components/columns'
import { DataTable } from './components/data-table'

export default function Dataset() {
  const [setupsData, setSetUpsData] = useState<
    { id: string; display_name: string; created_at: string, [key: string]: any }[]
  >([])
  const [setUpsParams, setSetUpsParams] = useState<{ page: number; page_size: number }>({
    page: 1,
    page_size : 10,
  });

  useEffect(() => {
    getSetUps(setUpsParams).then((res: any) => {
      setSetUpsData(res.data.data)
    })
  }, [])

  return (
      <Main>
        <div className='mb-2 flex flex-wrap items-center justify-between space-y-2 gap-x-4'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight'>Dataset</h2>
            <p className='text-muted-foreground'>
              Here&apos;s a list of your Data!
            </p>
          </div>
        </div>
        <div className='-mx-4 flex-1 overflow-auto px-4 py-1 lg:flex-row lg:space-y-0 lg:space-x-12'>
          <DataTable data={setupsData} columns={columns} />
        </div>
      </Main>

  )
}
