import { useForm } from 'react-hook-form'
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
  Sheet,
  SheetClose,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet'
import { createProvider, updateProvider } from '@/apis/turnbench'

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
      api_key: '',
      max_concurrent: 1,
      description: '',
    },
  })

  const onSubmit = (data: any) => {
    onOpenChange(false)
    form.reset()
    if (!isUpdate) {
      createProvider(data).then(() => {
        
      })
    } else {
      const { id, ...providerParams } = data
      updateProvider(id, providerParams).then(() => {

      })
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
              name='display_name'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Provider name</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a name' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name='base_url'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>base_url</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a base_url' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {!isUpdate && (<FormField
              control={form.control}
              name='api_key'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>api_key</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a api_key' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />)}
            <FormField
              control={form.control}
              name='max_concurrent'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>max_concurrent</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder='Enter a max_concurrent' />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
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
