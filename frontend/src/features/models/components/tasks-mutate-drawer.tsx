import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { createModel, getProviders, updateModel } from '@/apis/turnbench'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'

interface Props {
  open: boolean
  onOpenChange: (open: boolean) => void
  currentRow?: any
}

export function TasksMutateDrawer({ open, onOpenChange, currentRow }: Props) {
  const isUpdate = !!currentRow

  const form = useForm<any>({
    defaultValues: currentRow ?? {
      display_name: '',
      base_url: '',
      provider_id: '',
      max_concurrent: 1,
      description: '',
    },
  })

  const [providersData, setProvidersData] = useState<
    {
      id: string
      display_name: string
      created_at: string
      [key: string]: any
    }[]
  >([])
  const [providerParams, setProviderParams] = useState<{
    page: number
    page_size: number
  }>({
    page: 1,
    page_size: 100,
  })

  useEffect(() => {
    getProviders(providerParams).then((res: any) => {
      setProvidersData(res.data.data)
    })
  }, [])

  const onSubmit = (data: any) => {
    onOpenChange(false)
    form.reset()
    if (!isUpdate) {
      createModel(data).then(() => {})
    } else {
      const { id, ...modelParams } = data
      updateModel(id, modelParams).then(() => {})
    }
  }

  return (
    <Sheet
      open={open}
      onOpenChange={(v) => {
        onOpenChange(v)
        form.reset()
      }}
    >
      <SheetContent className='flex flex-col'>
        <SheetHeader className='text-left'>
          <SheetTitle>{isUpdate ? 'Update' : 'Create'}</SheetTitle>
        </SheetHeader>
        <Form {...form}>
          <form
            id='tasks-form'
            onSubmit={form.handleSubmit(onSubmit)}
            className='flex-1 space-y-5 px-4'
          >
            <FormField
              control={form.control}
              name='name'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Model name</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a name' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='display_name'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Model display name</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a display name' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name='frequency_penalty'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>frequency_penalty</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a frequency_penalty' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='presence_penalty'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>presence_penalty</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a presence_penalty' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='max_tokens'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>max_tokens</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a max_tokens' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='max_completion_tokens'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>max_completion_tokens</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder='Enter a max_completion_tokens'
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name='temperature'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>temperature</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a temperature' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='top_p'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>top_p</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a top_p' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='reasoning_effort'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>reasoning_effort</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a reasoning_effort' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {!isUpdate && (
              <FormField
                control={form.control}
                name='provider_id'
                render={({ field }) => (
                  <FormItem className='w-full space-y-1'>
                    <FormLabel>provider</FormLabel>
                    <FormControl>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger className='w-full'>
                            <SelectValue placeholder='Select a provider' />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {providersData.map((item: any) => (
                            <SelectItem key={item.id} value={item.id}>
                              {item.display_name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            )}
            <FormField
              control={form.control}
              name='description'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>description</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a description' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </form>
        </Form>
        <SheetFooter className='gap-2'>
          <SheetClose asChild>
            <Button variant='outline'>Close</Button>
          </SheetClose>
          <Button form='tasks-form' type='submit'>
            Save changes
          </Button>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  )
}
