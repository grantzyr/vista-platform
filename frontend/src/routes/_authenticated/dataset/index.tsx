import { createFileRoute } from '@tanstack/react-router'
import Dataset from '@/features/dataset'

export const Route = createFileRoute('/_authenticated/dataset/')({
  component: Dataset,
})
