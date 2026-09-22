#import <Foundation/Foundation.h>
#import <Vision/Vision.h>

int main(int argc, const char * argv[]) {
  @autoreleasepool {
    NSMutableDictionary *result=[NSMutableDictionary dictionary];
    for(int i=1;i<argc;i++){
      NSString *path=[NSString stringWithUTF8String:argv[i]];
      NSURL *url=[NSURL fileURLWithPath:path];
      VNRecognizeTextRequest *request=[[VNRecognizeTextRequest alloc] init];
      request.recognitionLevel=VNRequestTextRecognitionLevelFast;
      request.usesLanguageCorrection=NO;
      VNImageRequestHandler *handler=[[VNImageRequestHandler alloc] initWithURL:url options:@{}];
      NSError *error=nil; [handler performRequests:@[request] error:&error];
      NSMutableArray *lines=[NSMutableArray array];
      if(!error) for(VNRecognizedTextObservation *obs in request.results){VNRecognizedText *text=[[obs topCandidates:1] firstObject];if(text) [lines addObject:text.string];}
      result[path]=[lines componentsJoinedByString:@" "];
    }
    NSData *json=[NSJSONSerialization dataWithJSONObject:result options:0 error:nil];
    fwrite(json.bytes,1,json.length,stdout);
  }
  return 0;
}
