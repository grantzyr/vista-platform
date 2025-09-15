import { useEffect, useState } from 'react'
import { useRouter } from '@tanstack/react-router'
import { createSession, getSetUps, getllms } from '@/apis/turnbench'
import { CheckIcon, ChevronsUpDownIcon } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import { Label } from '@/components/ui/label'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

export default function Setups() {
  const [setUps, setSetUps] = useState<{ id: string }[]>([])
  const [models, setModels] = useState<{ id: string; display_name: string }[]>(
    []
  )
  const router = useRouter()

  const [openSetUp, setOpenSetUp] = useState(false)
  const [openModel, setOpenModel] = useState(false)
  const [selectModel, setSelectModel] = useState({
    id: '',
    display_name: '',
  })
  const [selectSetUp, setSelectSetUp] = useState('')
  const [selectMode, setSelectMode] = useState('classic')

  useEffect(() => {
    getSetUps({ page: 1, page_size: 100 }).then((res: any) => {
      setSetUps(res.data.data || [])
    })
    getllms({ page: 1, page_size: 100 }).then((res: any) => {
      setModels(res.data.data || [])
    })
  }, [])

  const handleStart = () => {
    const params = {
      mode: selectMode,
      llm_id: selectModel.id,
      setup_id: selectSetUp,
      max_rounds: 99,
    }
    // 创建 session 并跳转
    createSession(params).then((res: any) => {
      const sessionId = res.data.data.id
      router.navigate({
        to: '/session-detail/$session_id',
        params: { session_id: sessionId },
      })
    })
  }


  return (
    <div className='flex min-h-[60vh] flex-col items-center justify-center space-y-6'>
      <div className=''>Evaluation Setting</div>
      <div className='flex w-[500px]'>
        <Label className='mr-4'>Model:</Label>
        <Popover open={openModel} onOpenChange={setOpenModel}>
          <PopoverTrigger asChild>
            <Button
              variant='outline'
              role='combobox'
              aria-expanded={openModel}
              className='justify-between ml-[72px] w-[366px]'
            >
              {selectModel.display_name
                ? selectModel.display_name
                : 'Select model...'}
              <ChevronsUpDownIcon className='ml-2 h-4 w-4 shrink-0 opacity-50' />
            </Button>
          </PopoverTrigger>
          <PopoverContent className='p-0 w-[366px]'>
            <Command>
              <CommandInput placeholder='Search model...' />
              <CommandList>
                <CommandEmpty>No model found.</CommandEmpty>
                <CommandGroup>
                  {models.map((model) => (
                    <CommandItem
                      key={model.display_name}
                      value={model.display_name}
                      onSelect={(currentValue) => {
                        setSelectModel(
                          currentValue === selectModel.display_name
                            ? {
                                id: '',
                                display_name: '',
                              }
                            : model
                        )
                        setOpenModel(false)
                      }}
                    >
                      <CheckIcon
                        className={cn(
                          'mr-2 h-4 w-4',
                          selectModel.display_name === model.display_name
                            ? 'opacity-100'
                            : 'opacity-0'
                        )}
                      />
                      {model.display_name}
                    </CommandItem>
                  ))}
                </CommandGroup>
              </CommandList>
            </Command>
          </PopoverContent>
        </Popover>
      </div>

      <div className='flex w-[500px]'>
        <Label className='mr-4'>Data:</Label>
        <Popover open={openSetUp} onOpenChange={setOpenSetUp}>
          <PopoverTrigger asChild>
            <Button
              variant='outline'
              role='combobox'
              aria-expanded={openSetUp}
              className='justify-between ml-[82px] w-[366px]'
            >
              {selectSetUp
                ? setUps.find((setup) => setup.id === selectSetUp)?.id
                : 'Select Data...'}
              <ChevronsUpDownIcon className='ml-2 h-4 w-4 shrink-0 opacity-50' />
            </Button>
          </PopoverTrigger>
          <PopoverContent className='p-0 w-[366px]'>
            <Command>
              <CommandInput placeholder='Search setup...' />
              <CommandList>
                <CommandEmpty>No setup found.</CommandEmpty>
                <CommandGroup>
                  {setUps.map((setup) => (
                    <CommandItem
                      key={setup.id}
                      value={setup.id}
                      onSelect={(currentValue) => {
                        setSelectSetUp(
                          currentValue === selectSetUp ? '' : currentValue
                        )
                        setOpenSetUp(false)
                      }}
                    >
                      <CheckIcon
                        className={cn(
                          'mr-2 h-4 w-4',
                          selectSetUp === setup.id ? 'opacity-100' : 'opacity-0'
                        )}
                      />
                      {setup.id}
                    </CommandItem>
                  ))}
                </CommandGroup>
              </CommandList>
            </Command>
          </PopoverContent>
        </Popover>
      </div>

      <div className='flex w-[500px]'>
        <Label className='mr-4'>Evaluation Mode:</Label>
        <RadioGroup
          className='flex justify-between'
          defaultValue={selectMode}
          onValueChange={setSelectMode}
          orientation='horizontal'
        >
          <div className='flex items-center gap-3'>
            <RadioGroupItem value='classic' id='r1' />
            <Label htmlFor='r1'>classic</Label>
          </div>
          <div className='flex items-center gap-3'>
            <RadioGroupItem value='nightmare' id='r2' />
            <Label htmlFor='r2'>nightmare</Label>
          </div>
        </RadioGroup>
      </div>

      <div className='flex w-[500px] justify-between '>
        <Button className='space-x-1' onClick={() => {
          history.back()
        }}>
          <span>Back</span>
        </Button>
        <Button className='space-x-1' onClick={() => handleStart()}>
          <span>Continue</span>
        </Button>
      </div>
    </div>
  )
}
