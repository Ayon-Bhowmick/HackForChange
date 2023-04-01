import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import Map from "./views/Map.js"
import Add from "./views/Add.js"
import Login from "./views/Login.js"
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export default function App({navigation}) {
  return (
    <NavigationContainer>
		<Stack.Navigator initialRouteName="Home">
			<Stack.Screen name="Login" component={Login} />	
			<Stack.Screen name="Map" component={Map} />
			<Stack.Screen name="Add" component={Add} />
			
      	</Stack.Navigator>
    </NavigationContainer>
    
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: '100%',
    height: '100%',
  },
});