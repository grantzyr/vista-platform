import { createFileRoute } from '@tanstack/react-router'
import StartGame from '@/features/start-game'

export const Route = createFileRoute('/_authenticated/start-game/')({
  component: StartGame,
})
