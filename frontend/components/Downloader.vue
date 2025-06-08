<template>
  <div class="downloader">
    <div class="header">
      <h1>Facebook Downloader - AllxdDev</h1>
      <p>Tempel URL video Facebook Anda di bawah ini untuk mengunduh</p>
    </div>

    <div class="input-container">
      <div class="input-group">
        <input
          v-model="videoUrl"
          placeholder="Tempel URL video Facebook di sini"
          @keyup.enter="fetchVideo"
          class="url-input"
        />
        <!-- <button @click="pasteFromClipboard" class="paste-icon-btn">
          <i class="icon">📋</i>
        </button> -->
        <button 
          @click="fetchVideo" 
          class="action-btn download-btn"
          :disabled="!videoUrl || loading"
        >
          <span v-if="!loading">
            <i class="icon">⬇️</i> Download
          </span>
          <span v-else class="loading">
            <i class="icon">⏳</i> Processing...
          </span>
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="videoData" class="user-info-container">
      <div class="user-info-card">
        <div v-if="videoData.user" class="user-info">
          <img :src="videoData.user.avatar" class="user-avatar"/>
          <div>
            <div class="user-name">{{ videoData.user.name }}</div>
            <div class="video-title">{{ videoData.title }}</div>
          </div>
        </div>
        <div v-else class="video-title">{{ videoData.title }}</div>
      </div>

      <div class="quality-options">
        <div class="quality-card video-quality">
          <h4><i class="icon">🎬</i> Video Quality</h4>
          <div class="video-preview">
            <video 
              v-if="videoData.previewUrl"
              :src="videoData.previewUrl"
              controls
              class="video-player"
            >
              <source :src="videoData.previewUrl" type="video/mp4">
            </video>
          </div>
          <div class="quality-buttons">
            <button 
              v-for="(video, index) in videoData.videos" 
              :key="'video-'+index"
              @click="downloadFile(video.url)"
              class="quality-btn"
              :class="{ 'downloading': downloading && currentDownloadUrl === video.url }"
              :disabled="downloading"
              :style="{'--progress': `${downloadProgress}%`}"
            >
              <span>
                {{ video.quality }}
                <span v-if="downloading && currentDownloadUrl === video.url" class="loading-text">
                  ({{ downloadProgress }}%)
                </span>
              </span>
            </button>
          </div>
        </div>
        
        <div class="quality-card audio-quality">
          <h4><i class="icon">🎵</i> Audio Only</h4>
          <div class="quality-buttons">
            <button 
              v-for="(audio, index) in videoData.audios" 
              :key="'audio-'+index"
              @click="downloadFile(audio.url)"
              class="quality-btn"
              :class="{ 'downloading': downloading && currentDownloadUrl === audio.url }"
              :disabled="downloading"
              :style="{'--progress': `${downloadProgress}%`}"
            >
              <span>
                {{ audio.quality }}
                <span v-if="downloading && currentDownloadUrl === audio.url" class="loading-text">
                  ({{ downloadProgress }}%)
                </span>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Downloader',
  data() {
    return {
      videoUrl: '',
      videoData: null,
      loading: false,
      error: null,
      downloading: false,
      currentDownloadUrl: null,
      downloadProgress: 0
    }
  },
  methods: {
    async pasteFromClipboard() {
      try {
        const text = await navigator.clipboard.readText()
        this.videoUrl = text
      } catch (err) {
        this.error = 'Failed to access clipboard. Please paste manually.'
        console.error('Failed to read clipboard:', err)
      }
    },
    async fetchVideo() {
      if (!this.videoUrl) return
      
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('https://fb-downloader-be-2.vercel.app/fetch', {
          url: this.videoUrl
        })
        
        // Process API response
        const apiData = response.data.api
        this.videoData = {
          title: apiData.title,
          previewUrl: apiData.previewUrl,
          thumbnail: apiData.imagePreviewUrl,
          user: apiData.userInfo ? {
            name: apiData.userInfo.name,
            avatar: apiData.userInfo.userAvatar
          } : null,
          videos: apiData.mediaItems
            .filter(item => item.type === 'Video')
            .map(video => ({
              quality: `${video.mediaRes} (${video.mediaQuality}) - ${video.mediaFileSize}`,
              url: video.mediaUrl
            })),
          audios: apiData.mediaItems
            .filter(item => item.type === 'Audio')
            .map(audio => ({
              quality: `${audio.mediaQuality} - ${audio.mediaFileSize}`,
              url: audio.mediaUrl
            }))
        }
      } catch (error) {
        this.error = 'Failed to fetch video info. Please check the URL and try again.'
        console.error('Error fetching video:', error)
      } finally {
        this.loading = false
      }
    },
    async downloadFile(url) {
      try {
        this.error = null
        this.downloading = true
        this.currentDownloadUrl = url
        this.downloadProgress = 0
        let modal = null
        
        if (this.$modal && this.$modal.show) {
          modal = this.$modal.show({
            title: 'Preparing Download',
            content: 'Fetching download link...',
            showProgress: false
          })
        }

        // First fetch the download info
        this.downloadProgress = 95
        const response = await axios.get(url)
        const data = response.data
        
        if (!data.fileUrl) {
          throw new Error('No download URL found')
        }

        // Simulate realistic progress with random variations
        const interval = setInterval(() => {
          if (this.downloadProgress < 100) {
            // Random increment between 1-5% with occasional pauses
            const increment = Math.random() < 0.8 ? 
              Math.floor(Math.random() * 5) + 1 : 0
            this.downloadProgress = Math.min(
              this.downloadProgress + increment, 
              100
            )
            
            // Random speed variations
            const delay = Math.random() < 0.7 ? 
              200 + Math.floor(Math.random() * 300) : 
              500 + Math.floor(Math.random() * 1000)
            
            clearInterval(interval)
            setTimeout(() => {
              const newInterval = setInterval(() => {
                if (this.downloadProgress < 100) {
                  const newIncrement = Math.random() < 0.8 ? 
                    Math.floor(Math.random() * 5) + 1 : 0
                  this.downloadProgress = Math.min(
                    this.downloadProgress + newIncrement, 
                    100
                  )
                } else {
                  clearInterval(newInterval)
                }
              }, delay)
            }, delay)
          } else {
            clearInterval(interval)
          }
        }, 300)

        if (modal && modal.update) {
          modal.update({
            content: 'Starting download...',
            showProgress: false
          })
        }

        // Create download link
        const link = document.createElement('a')
        link.href = data.fileUrl
        link.download = data.fileName || 'facebook_video.mp4'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        // Complete progress
        this.downloadProgress = 100
        
        if (modal && modal.close) {
          setTimeout(() => {
            modal.close()
          }, 1500)
        }
      } catch (error) {
        this.error = 'Download failed. Please try again.'
        console.error('Download error:', error)
        
        if (this.$modal && this.$modal.show) {
          this.$modal.show({
            title: 'Download Failed',
            content: this.error,
            isError: true
          })
        }
      } finally {
        this.downloading = false
        this.currentDownloadUrl = null
      }
    }
  }
}
</script>

<style scoped>
:root {
  --primary: #4267B2;
  --secondary: #898F9C;
  --accent: #FF7B00;
  --light: #F0F2F5;
  --dark: #1C1E21;
  --success: #42B72A;
  --danger: #FA3E3E;
}

.downloader {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  color: var(--dark);
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.header p {
  color: var(--secondary);
}

.input-container {
  margin-bottom: 2rem;
}

.input-group {
  display: flex;
  gap: 0.5rem;
}

.url-input {
  flex-grow: 1;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
}

.url-input:focus {
  border-color: var(--primary);
  outline: none;
  box-shadow: 0 0 0 2px rgba(66, 103, 178, 0.2);
}

.input-group {
  position: relative;
  display: flex;
  width: 100%;
  gap: 0.5rem;
}

.url-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
  min-width: 0;
  padding-right: 2.5rem; /* Space for paste button */
}

.paste-icon-btn {
  position: absolute;
  right: 110px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--secondary);
  z-index: 2;
  padding: 0.5rem;
}

.action-btn {
  width: auto;
  padding: 0.75rem 1.5rem;
  white-space: nowrap;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .url-input {
    padding-right: 2rem;
  }
  .paste-icon-btn {
    right: 100px;
  }
  .action-btn {
    padding: 0.75rem 1rem;
  }
}

.paste-icon-btn:hover {
  color: var(--primary);
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}


.download-btn {
  background: #365899;
  color: white;
}

.download-btn:hover:not(:disabled) {
  background: #2d4a7d;
}

.download-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: var(--danger);
  background: rgba(250, 62, 62, 0.1);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
}

.video-container {
  margin-top: 2rem;
  animation: fadeIn 0.3s ease-out;
}

.video-preview {
  text-align: center;
  margin-bottom: 1.5rem;
}

.video-player {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: #000;
  margin-bottom: 1rem;
}

.video-title {
  color: var(--dark);
  margin: 0.5rem 0;
}

.user-info-container {
  margin-top: 1rem;
}

.user-info-card {
  background: #f8fafc;
  padding: 1.0rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  font-weight: 600;
  color: var(--dark);
  font-size: 1rem;
  text-align: left;
}

.video-title {
  color: var(--secondary);
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.paste-icon-btn {
  background: transparent;
  border: none;
  padding: 0 0.5rem;
  cursor: pointer;
  color: var(--secondary);
}

.paste-icon-btn:hover {
  color: var(--primary);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-size: 0.9rem;
  color: var(--secondary);
}

.quality-options {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
  align-items: flex-start;
}

.quality-card.video-quality {
  flex: 6;
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.video-player {
  width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: #000;
  margin-bottom: 1rem;
}

.quality-card.audio-quality {
  flex: 4;
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.quality-card h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quality-card .video-title {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  color: var(--dark);
}


.quality-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
}

.quality-btn {
  padding: 0.75rem;
  background: #e2e8f0;
  border: 1px solid #cbd5e0;
  border-radius: 8px;
  color: #2d3748;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.quality-btn:hover {
  background: #cbd5e0;
  color: #2d3748;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quality-btn.downloading {
  color: white;
}

.quality-btn.downloading::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: var(--progress, 0%);
  background: linear-gradient(to right, #365899, #42B72A);
  transition: width 0.3s ease;
  z-index: 0;
}

.quality-btn.downloading span {
  position: relative;
  z-index: 1;
}

.icon {
  font-size: 1.2em;
}

.loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .input-group {
    flex-direction: column;
  }
  
  .quality-options {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
