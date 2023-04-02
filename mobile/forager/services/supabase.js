import AsyncStorage from '@react-native-async-storage/async-storage'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = "https://uqbtapuvxtlwukbznngm.supabase.co"
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVxYnRhcHV2eHRsd3VrYnpubmdtIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODA0MTA4MjYsImV4cCI6MTk5NTk4NjgyNn0.fse_zLqZuaY75iqSNyfEgyqCylov4b989WatrIQ13wo"
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        storage: AsyncStorage
    }
})