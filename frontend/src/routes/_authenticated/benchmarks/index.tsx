import { createFileRoute } from '@tanstack/react-router'
import Benchmarks from '@/features/benchmarks'

export const Route = createFileRoute('/_authenticated/benchmarks/')({
  component: Benchmarks,
})
