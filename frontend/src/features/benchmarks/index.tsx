'use client'

import { useEffect, useState } from 'react'
import { useRouter } from '@tanstack/react-router'
import { getGames } from '@/apis/turnbench'
import { ChevronRightIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Main } from '@/components/layout/main'

export default function Benchmarks() {
  const router = useRouter()
  const [gamesData, setGamesData] = useState<
    {
      id: string
      display_name: string
      created_at: string
      [key: string]: any
    }[]
  >([])
  const [gameParams, setGameParams] = useState<{
    page: number
    page_size: number
  }>({
    page: 1,
    page_size: 10,
  })
  useEffect(() => {
    getGames(gameParams).then((res: any) => {
      setGamesData(res.data.data)
    })
  }, [])

  const playGame = (game: any) => {
    sessionStorage.setItem('gameid', game.id)
    router.navigate({ to: '/dataset' })
  }

  return (
    <>
      <Main>
        <div className='absolute top-[16px] text-[24px] font-semibold'>VISTA</div>
        <div className='mb-2 flex flex-wrap items-center justify-between space-y-2 gap-x-4'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight'>Benchmarks</h2>
            <p className='text-muted-foreground'>
              Here&apos;s a list of your Benchmarks!
            </p>
          </div>
        </div>
        <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
          {gamesData.map((game) => (
            <Card>
              <CardHeader className='flex flex-col space-y-0 pb-2'>
                <div className='flex w-full flex-row items-center justify-between'>
                  <CardTitle className='text-base font-medium'>
                    {game.display_name}
                  </CardTitle>
                  <Button
                    variant='secondary'
                    size='icon'
                    className='size-8'
                    onClick={() => playGame(game)}
                  >
                    <ChevronRightIcon />
                  </Button>
                </div>
                <div>
                  <p className='text-muted-foreground text-xs'>
                    {game.description}
                  </p>
                </div>
              </CardHeader>
              <CardContent>
                <p className='text-muted-foreground text-xs'>
                  Last update at: {new Date(game.created_at).toLocaleString()}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </Main>
    </>
  )
}
