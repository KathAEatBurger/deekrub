import { supabase } from './supabase_client.js'

async function getData() {
  const { data, error } = await supabase.from('your_table').select('*')
  if (error) {
    console.error('Error:', error)
  } else {
    console.log('Data:', data)
  }
}

getData()
