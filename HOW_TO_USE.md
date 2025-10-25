# How to Use JamaAlca - AI-Powered Farming App

## 🚀 **Getting Started**

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Run the Application**
```bash
python jamaalca.py
```

## 📱 **Using the App**

### **🏠 Home Screen**
- **What it shows**: Your farm's current status, weather, and sustainability metrics
- **What you can do**: See how much water you've saved, how your crops are doing, and get daily farming tips
- **Navigation**: Click the buttons at the bottom to go to different sections

### **🌿 Plant Detection Screen**
- **What it does**: Takes photos of your plants and tells you if they're healthy or sick
- **How to use**:
  1. Select the type of crop (Tomato, Corn, Potato, Wheat)
  2. Click "Capture / Upload Image" to choose a photo
  3. Wait for the AI to analyze the photo
  4. Get treatment recommendations if there's a disease

### **🌤 Weather Screen**
- **What it shows**: 7-day weather forecast and farming recommendations
- **What you can do**: See if you need to water your plants, prepare for rain, or protect from drought
- **Smart alerts**: The app warns you about drought, heavy rain, or other weather problems

### **👩🏾‍🌾 Community Screen**
- **What it is**: A forum where farmers can ask questions and share advice
- **How to use**:
  1. Browse existing discussions by category
  2. Search for specific topics
  3. Start your own discussion
  4. Reply to other farmers' questions

### **🔔 Alerts Screen**
- **What it shows**: All your notifications and alerts
- **Types of alerts**: Weather warnings, watering reminders, disease alerts, market updates

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the JamaAlca folder with your API keys:

```env
# Azure OpenAI (for treatment recommendations)
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_KEY=your_key_here
DEPLOYMENT_NAME=your_deployment_name

# Azure Vision (for disease detection)
AZURE_VISION_ENDPOINT=your_vision_endpoint
AZURE_VISION_PREDICTION_KEY=your_prediction_key
AZURE_VISION_PROJECT_ID=your_project_id
AZURE_VISION_PUBLISHED_NAME=your_published_name

# App Settings
USE_REAL_DATA=True
DEBUG=False
```

### **Using Fake Data for Testing**
Set `USE_REAL_DATA=False` in your `.env` file to use demonstration data instead of real APIs.

## 🛠 **Troubleshooting**

### **Common Issues**

1. **"ModuleNotFoundError: No module named 'dotenv'"**
   - The app will work without dotenv, but you can install it: `pip install python-dotenv`

2. **GPS Error Messages**
   - This is normal - the app will use your IP address to get your location instead

3. **Weather Data Errors**
   - The app will fall back to dummy weather data if the API fails

4. **Image Analysis Fails**
   - Make sure you select a crop type before analyzing
   - Use common image formats (JPG, PNG)
   - Check your internet connection for AI services

### **Getting Help**
- Check the console output for error messages
- Make sure all API keys are correctly set
- Ensure you have a stable internet connection

## 🎯 **Tips for Best Results**

1. **Take Clear Photos**: Good lighting and clear focus help the AI detect diseases better
2. **Select Correct Crop Type**: This helps the AI give more accurate results
3. **Check Weather Regularly**: The app gives better advice when it knows the weather conditions
4. **Use Community Features**: Other farmers can help with specific problems
5. **Save Your Results**: The app remembers your scans to track your progress

## 🔮 **Future Features**
- Real-time market prices
- Soil analysis recommendations
- Crop yield predictions
- SMS alerts for critical issues
- Resource sharing marketplace

---

**Happy Farming! 🌱**
